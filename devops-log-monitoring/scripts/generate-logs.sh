#!/usr/bin/env bash
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8080}"
for i in $(seq 1 10); do
  curl -fsS "$BASE_URL/work" >/dev/null
  curl -fsS "$BASE_URL/demo/random-log" || true
  sleep 1
done
echo "Requests generated; inspect app logs and Grafana/Loki."
