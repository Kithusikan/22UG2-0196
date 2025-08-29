# CCS3308 Assignment 1 – Dockerized Web App (Flask + Postgres)

This repository contains a minimal **two‑service web application** that satisfies the assignment requirements:

- Two services: `web` (Flask) and `db` (PostgreSQL).
- Each service listens on its own port (`web`: 5000, `db`: 5432 mapped to host 5433).
- Services run in separate containers and communicate over a Docker network.
- The database persists state using a **named volume** `ccs3308_db_data`.

> Replace `<your_registration_number>` in your GitHub repository name as required by the assignment.

---

## 1) Deployment Requirements

- Docker (20+ recommended)  
- Docker Compose v2 (usually available via `docker compose`; `docker-compose` also supported)
- Internet access to pull Docker images

---

## 2) Application Description

A tiny Flask app connects to PostgreSQL and keeps a persistent **page visit counter**. Each page refresh increments the counter stored in the database.

- Web UI: `http://localhost:5000`
- Database exposed on host: `localhost:5433` (container 5432)

---

## 3) Network and Volume Details

- **Network:** `ccs3308_app_net` – an isolated bridge network for inter‑container communication.  
- **Named Volume:** `ccs3308_db_data` – mounted at `/var/lib/postgresql/data` in the `db` container for persistent PostgreSQL data.

---

## 4) Container Configuration

### `db` (PostgreSQL 16)
- Image: `postgres:16-alpine`
- Ports: `5433:5432` (host:container)
- Env:
  - `POSTGRES_USER=app`
  - `POSTGRES_PASSWORD=app_pw`
  - `POSTGRES_DB=appdb`
- Healthcheck: `pg_isready`

### `web` (Flask on Python 3.12-slim)
- Build context: `./web`
- Ports: `5000:5000`
- Env:
  - `DATABASE_URL=postgresql://app:app_pw@db:5432/appdb`
  - `FLASK_RUN_HOST=0.0.0.0`
  - `FLASK_RUN_PORT=5000`

---

## 5) Container List

| Container | Role | Exposed Port(s) |
| --- | --- | --- |
| `db` | PostgreSQL database (persistent) | 5433 (host) → 5432 (container) |
| `web` | Flask web app (talks to `db`) | 5000 |

---

## 6) Instructions

> First time only (after cloning/unzipping): mark scripts executable
>
> ```bash
> chmod +x *.sh
> ```

### Prepare (create network/volume, build images)

```bash
./prepare-app.sh
```

### Run (start the stack)

```bash
./start-app.sh
# Output: "The app is available at http://localhost:5000"
```

Open your browser at **http://localhost:5000**.

### Pause (stop containers without losing data)

```bash
./stop-app.sh
```

### Delete (remove containers, images, networks, volumes)

```bash
./remove-app.sh
```

> **Note:** `remove-app.sh` deletes the named volume, so the counter resets next time.

---

## 7) Example Workflow

```bash
# Create application resources
./prepare-app.sh
Preparing app ...
Done.

# Run the application
./start-app.sh
Running app ...
The app is available at http://localhost:5000

# Open a web browser and interact with the application

# Pause the application
./stop-app.sh
Stopping app ...

# Delete all application resources
./remove-app.sh
Removing all application resources ...
Removed app.
```

---

## 8) How it works (quick overview)

- On first request, the Flask app ensures a `counters` table exists and initializes the `hits` row.
- Every page view runs `UPDATE counters SET value = value + 1 WHERE key='hits' RETURNING value;` and shows the current counter.
- Data is stored on the `ccs3308_db_data` **named volume**, so stopping/starting the app does not reset the counter.

---

## 9) Submission checklist

- Repository is **public** and named **`<your_registration_number>`**.
- Contains these files:
  - `prepare-app.sh`, `start-app.sh`, `stop-app.sh`, `remove-app.sh`
  - `docker-compose.yaml`
  - `README.md`
  - `web/` folder with app code and Dockerfile
- The app runs and meets the rubric (usability, completeness, functionality, documentation, clarity, originality).
