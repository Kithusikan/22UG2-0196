import os
import psycopg2
from flask import Flask

app = Flask(__name__)

DB_URL = os.environ.get("DATABASE_URL", "postgresql://app:app_pw@db:5432/appdb")

def get_conn():
    return psycopg2.connect(DB_URL)

def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS counters (
                    key TEXT PRIMARY KEY,
                    value INTEGER NOT NULL
                );
            """)
            cur.execute("""
                INSERT INTO counters (key, value)
                VALUES ('hits', 0)
                ON CONFLICT (key) DO NOTHING;
            """)
    print("Database initialized.")

@app.route("/health")
def health():
    return "ok", 200

@app.route("/")
def index():
    # ensure table exists (first request after startup)
    init_db()
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE counters SET value = value + 1 WHERE key = 'hits' RETURNING value;")
            count = cur.fetchone()[0]
    html = f"""
    <html>
    <head><title>Flask + PostgreSQL (CCS3308)</title></head>
    <body style="font-family: sans-serif; max-width: 640px; margin: 40px auto;">
      <h1>Flask + PostgreSQL</h1>
      <p>This page has been viewed <strong>{count}</strong> times.</p>
      <p>Data is persisted in a Docker named volume (<code>ccs3308_db_data</code>).</p>
      <hr/>
      <p>Try stopping and starting the app; the counter will not reset.</p>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    host = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_RUN_PORT", "5000"))
    app.run(host=host, port=port)
