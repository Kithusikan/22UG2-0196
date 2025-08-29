#!/usr/bin/env bash
set -euo pipefail
compose() {
  if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    docker compose "$@"
  elif command -v docker-compose >/dev/null 2>&1; then
    docker-compose "$@"
  else
    echo "Error: Docker Compose is not installed." >&2
    exit 1
  fi
}
PROJECT="ccs3308"


echo "Removing all application resources ..."
compose -p "$PROJECT" down --rmi all -v || true

docker volume rm ccs3308_db_data >/dev/null 2>&1 || true
docker network rm ccs3308_app_net >/dev/null 2>&1 || true

echo "Removed app."
