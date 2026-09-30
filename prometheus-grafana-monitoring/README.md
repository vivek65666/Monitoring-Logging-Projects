# Flask Observability & Monitoring Suite

![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-Metrics-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana&logoColor=white)
![Python](https://img.shields.io/badge/Python-Flask-3776AB?logo=python&logoColor=white)

A containerized observability stack for a Flask application using **Prometheus** and **Grafana**. The project demonstrates custom metrics instrumentation, Prometheus scraping, PromQL querying, and Grafana dashboard design, all started with a single `docker-compose up` command.

---

## Table of Contents

- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Metrics Exposed](#metrics-exposed)
- [Example PromQL Queries](#example-promql-queries)
- [Grafana Dashboard](#grafana-dashboard)
- [Generating Traffic](#generating-traffic)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)
- [What I Learned](#what-i-learned)
- [Author](#author)

---

## Architecture

```
+-------------------------------------------------------------+
|                    Docker Compose Network                   |
|                                                             |
|   +----------------+   scrapes /metrics   +--------------+  |
|   |   Flask App    | <------------------- |  Prometheus  |  |
|   |  (port 5000)   |      over HTTP       |  (port 9090) |  |
|   +----------------+                      +------+-------+  |
|                                                  |          |
|                                          PromQL  |          |
|                                          queries |          |
|                                                  v          |
|                                           +-------------+   |
|                                           |   Grafana   |   |
|                                           | (port 3000) |   |
|                                           +-------------+   |
+-------------------------------------------------------------+
```

**Data flow**

1. **Instrumentation:** the Flask app uses `prometheus-client` to record HTTP metrics and exposes them at `/metrics`.
2. **Scraping:** Prometheus pulls metrics from the Flask container at a fixed interval and stores them as time series.
3. **Visualization:** Grafana uses Prometheus as a data source and renders dashboards from PromQL queries.

---

## Features

- Custom Flask HTTP metrics exposed on a `/metrics` endpoint
- Pull-based metrics collection with Prometheus
- Grafana dashboards for request rate and error rate
- PromQL queries using `rate()` and regex filters on status codes (4xx / 5xx / 404)
- Fully containerized setup with Docker Compose
- Reproducible: one command starts the whole stack

---

## Tech Stack

| Layer | Technology |
|---|---|
| Application | Python, Flask |
| Instrumentation | `prometheus-client` |
| Metrics storage | Prometheus |
| Visualization | Grafana |
| Containerization | Docker, Docker Compose |

---

## Project Structure

```
prometheus-grafana-monitoring/
├── app/                    # Flask application and Dockerfile
├── prometheus/             # Prometheus configuration (prometheus.yml)
├── docker-compose.yml      # Runs Flask, Prometheus and Grafana
└── README.md
```

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Git

### 1. Clone the repository

```bash
git clone https://github.com/vivek65666/Monitoring-Logging-Projects.git
cd Monitoring-Logging-Projects/prometheus-grafana-monitoring
```

### 2. Start the stack

```bash
docker-compose up -d
```

If your Docker version uses the newer plugin syntax, run `docker compose up -d` instead.

### 3. Verify the containers are running

```bash
docker-compose ps
```

### 4. Access the services

| Service | URL | Notes |
|---|---|---|
| Flask app | http://localhost:5000 | Sample application |
| Flask metrics | http://localhost:5000/metrics | Raw Prometheus metrics |
| Prometheus | http://localhost:9090 | Check **Status > Targets** to confirm the Flask target is **UP** |
| Grafana | http://localhost:3000 | Default login: `admin` / `admin` (change on first login) |

### 5. Connect Grafana to Prometheus (if not auto-provisioned)

1. Open Grafana and go to **Connections > Data sources > Add data source**.
2. Choose **Prometheus**.
3. Set the URL to `http://prometheus:9090` (the Compose service name).
4. Click **Save & test**.

### 6. Stop the stack

```bash
docker-compose down
```

---

## Metrics Exposed

| Metric | Type | Description |
|---|---|---|
| `flask_http_requests_total` | Counter | Total HTTP requests, labelled by method, endpoint and status code |

---

## Example PromQL Queries

**Request rate per second (5-minute window)**

```promql
rate(flask_http_requests_total[5m])
```

**Request rate grouped by endpoint**

```promql
sum by (endpoint) (rate(flask_http_requests_total[5m]))
```

**Error rate (4xx and 5xx responses)**

```promql
sum(rate(flask_http_requests_total{status=~"4..|5.."}[5m]))
```

**404 responses only**

```promql
rate(flask_http_requests_total{status="404"}[5m])
```

> Label names (`endpoint`, `status`) depend on how they are defined in `app/`. Adjust the queries if your labels differ.

---

## Grafana Dashboard

The dashboard contains two main panels:

- **Flask Request Rate:** incoming requests per second, split by method and endpoint.
- **Flask Error Rate:** 4xx and 5xx responses over time, to spot client or server errors quickly.

### Dashboard preview

<!-- Add your screenshot to a screenshots/ folder, then uncomment the line below -->
<!-- ![Grafana Dashboard](screenshots/grafana-dashboard.png) -->

---

## Generating Traffic

To see the graphs move, generate some requests, including a few errors:

```bash
# Normal requests
for i in $(seq 1 100); do curl -s -o /dev/null http://localhost:5000/; done

# 404 errors
for i in $(seq 1 30); do curl -s -o /dev/null http://localhost:5000/does-not-exist; done
```

Refresh the Grafana dashboard after a few seconds to see the request and error rates change.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Prometheus target shows **DOWN** | Check the scrape target name and port in `prometheus/prometheus.yml`, and confirm the Flask container is running with `docker-compose ps` |
| Grafana shows **No data** | Confirm the data source URL is `http://prometheus:9090` and that requests were generated recently |
| Port already in use | Stop the process using ports 5000, 9090 or 3000, or change the host port in `docker-compose.yml` |
| Changes to the app are not reflected | Rebuild with `docker-compose up -d --build` |
| View container logs | `docker-compose logs -f <service-name>` |

---

## Future Improvements

- [ ] Add **node-exporter** for host CPU, memory and disk metrics
- [ ] Add **Prometheus alert rules** (for example, high error rate) and **Alertmanager** notifications
- [ ] Add latency metrics using a histogram
- [ ] Provision Grafana data sources and dashboards as code
- [ ] Persist Prometheus and Grafana data with Docker volumes
- [ ] Deploy the stack on Kubernetes using the `kube-prometheus-stack` Helm chart

---

## What I Learned

- How Prometheus pull-based scraping works and how targets are configured
- Instrumenting a Python application with custom metrics
- Writing PromQL queries with `rate()`, label filters and regex matching
- Building Grafana dashboards from Prometheus data
- Orchestrating a multi-container stack with Docker Compose

---

## Author

**Vivek C Raj**

- GitHub: [vivek65666](https://github.com/vivek65666)
- LinkedIn: [vivek-c-raj](https://www.linkedin.com/in/vivek-c-raj/)
