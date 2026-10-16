<div align="center">

# 🚨 DevOps Log Monitoring & Auto-Healing Platform

### Detect failures. Explore logs. Monitor metrics. Alert. Recover safely.

**A beginner-friendly, production-style learning project by [@the.devops111](https://www.instagram.com/the.devops111/)**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Probes-326CE5?logo=kubernetes&logoColor=white)
![Observability](https://img.shields.io/badge/Observability-Prometheus%20%7C%20Grafana%20%7C%20Loki-E6522C)

**Build → Break → Debug → Recover → Learn**

</div>

---

## 📚 Contents
1. [Project overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Repository structure](#3-repository-structure)
4. [Prerequisites](#4-prerequisites)
5. [Run locally](#5-run-locally)
6. [Failure and recovery lab](#6-failure-and-recovery-lab)
7. [Tests](#7-tests)
8. [Docker](#8-docker)
9. [Monitoring stack](#9-monitoring-stack)
10. [Kubernetes deployment](#10-kubernetes-deployment)
11. [GitHub Actions](#11-github-actions)
12. [Terraform starter](#12-terraform-starter)
13. [Troubleshooting](#13-troubleshooting)
14. [Production safety notes](#14-production-safety-notes)
15. [Interview questions](#15-interview-questions)

## 1. Project overview

A container being `Running` does not guarantee that users can use an application successfully. Engineers need to inspect health checks, logs, metrics, Service endpoints and alert signals before choosing a safe recovery action.

This repository contains a small Flask service that emits structured JSON logs, exposes Prometheus metrics, has liveness/readiness endpoints, and lets you deliberately simulate an HTTP error or unhealthy readiness state. It also includes Docker, Docker Compose, Kubernetes manifests, monitoring configuration, CI, and a safe Terraform exercise.

> **Honest auto-healing note:** this project teaches platform recovery behavior, not magic root-cause repair. Kubernetes removes a pod from ready Service endpoints when its readiness probe fails and restarts a container when its liveness probe repeatedly fails. The demo intentionally keeps liveness healthy during its simulated readiness failure, so you can observe and recover manually.

## 2. Architecture

```mermaid
flowchart LR
    A[Python Flask App] --> B[Docker]
    B --> C[Kubernetes]
    A --> D[JSON Logs]
    A --> E[/metrics]
    E --> F[Prometheus]
    F --> G[Grafana]
    D --> H[Promtail]
    H --> I[Loki]
    I --> G
    F --> J[Alert Rules]
    C --> K[Readiness / Liveness]
    J --> L[Investigate and Recover]
```

| Technology | Role |
|---|---|
| Python + Flask | Demo API, sample failures and health endpoints |
| Docker | Package the application |
| Kubernetes | Run replicas and evaluate probes |
| Prometheus | Scrape metrics and evaluate alert rules |
| Grafana | Explore metrics and logs |
| Loki + Promtail | Collect/query container logs in the local demo |
| GitHub Actions | Run tests and build the image |
| Terraform | Practice infrastructure-as-code safely |

## 3. Repository structure

```text
devops-log-monitoring/
├── app/                 # main.py, health.py, logger.py
├── tests/               # test_health.py
├── Dockerfile
├── docker-compose.yml
├── kubernetes/          # namespace, deployment, service, probes
├── monitoring/
│   ├── prometheus.yml
│   ├── grafana/         # dashboard and data-source provisioning
│   └── loki/            # Loki and Promtail configuration
├── alerts/              # Prometheus alert rules
├── .github/workflows/   # CI workflow
├── terraform/           # safe local-provider starter
├── scripts/             # log generation and health check
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## 4. Prerequisites

Required for the local app: Python 3.12+, pip and curl. For containers and monitoring, install Docker with the Compose plugin. Kubernetes and Terraform are optional until those sections.

```bash
python --version
pip --version
docker --version
docker compose version
kubectl version --client    # optional
terraform version           # optional
```

## 5. Run locally

### Linux / macOS

```bash
git clone <YOUR_REPOSITORY_URL>
cd devops-log-monitoring
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python -m app.main
```

### Windows PowerShell

```powershell
git clone <YOUR_REPOSITORY_URL>
cd devops-log-monitoring
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
python -m app.main
```

The app listens at `http://localhost:8080`.

```bash
curl http://localhost:8080/
curl http://localhost:8080/health/live
curl http://localhost:8080/health/ready
curl http://localhost:8080/metrics
curl http://localhost:8080/work
curl -i http://localhost:8080/simulate-error
```

`/simulate-error` intentionally returns HTTP 500; use it only in this learning environment.

## 6. Failure and recovery lab

**A. Confirm readiness**

```bash
curl -i http://localhost:8080/health/ready
```

Expected: HTTP 200.

**B. Simulate an unhealthy application state**

```bash
curl -X POST http://localhost:8080/simulate-failure
curl -i http://localhost:8080/health/ready
```

Expected: readiness returns HTTP 503.

**C. Recover manually**

```bash
curl -X POST http://localhost:8080/recover
curl -i http://localhost:8080/health/ready
```

Expected: readiness returns HTTP 200 again.

**D. Generate sample log activity**

```bash
bash scripts/generate-logs.sh
```

Or call `/work` and `/demo/random-log` repeatedly with curl. Inspect logs with `docker compose logs -f app` after starting Compose.

## 7. Tests

```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
```

Tests cover liveness, readiness, the failure/recovery flow and the metrics endpoint.

## 8. Docker

```bash
docker build -t devops-log-monitoring:local .
docker run --rm --name log-monitoring-app -p 8080:8080 devops-log-monitoring:local
```

In another terminal:

```bash
curl http://localhost:8080/health/ready
docker logs -f log-monitoring-app
```

## 9. Monitoring stack

Start the application, Prometheus, Grafana, Loki and Promtail:

```bash
docker compose up --build -d
docker compose ps
docker compose logs -f app
```

| Service | Local URL | Demo login |
|---|---|---|
| Application | http://localhost:8080 | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | `admin` / `admin` |
| Loki API | http://localhost:3100 | — |

**Local demo only:** change Grafana's sample password before exposing the service outside your own machine. Never commit production credentials.

Stop services:

```bash
docker compose down
```

Use `docker compose down -v` only if you intentionally want to discard local container volumes.

### Prometheus

Open `http://localhost:9090`, choose **Status → Targets**, and confirm `log-monitoring-app` is `UP`. Try:

```promql
sum(rate(demo_http_requests_total[5m])) by (status)
```

Generate an error with `curl -i http://localhost:8080/simulate-error`, wait for a scrape, then check the query again.

### Grafana

Open `http://localhost:3000`, sign in with the local demo credentials, and look for the **DevOps Demo** folder. The provisioned dashboard displays request-rate panels. If data is initially empty, generate requests and wait at least one scrape interval.

### Loki

In Grafana, open **Explore**, choose Loki and try:

```logql
{container=~".*log-monitoring.*"}
```

Docker log discovery can vary by operating system and Docker permissions. If logs do not appear, inspect `docker compose logs promtail loki` and verify the app emits logs with `docker compose logs app`.

### Alert rule

`alerts/alert-rules.yml` contains a learning rule for HTTP 5xx responses. A Prometheus rule by itself does **not** notify a human; configure Alertmanager and a notification receiver separately if you extend the project.

## 10. Kubernetes deployment

Build the image where your local cluster can access it:

```bash
docker build -t devops-log-monitoring:local .
```

For kind:

```bash
kind load docker-image devops-log-monitoring:local
```

For minikube:

```bash
minikube image load devops-log-monitoring:local
```

Apply manifests:

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl get pods -n log-monitoring
kubectl get svc -n log-monitoring
```

Forward the service port:

```bash
kubectl port-forward -n log-monitoring svc/devops-log-monitoring 8080:80
```

Then test `curl http://localhost:8080/health/ready`.

### Debugging commands

```bash
kubectl get pods -n log-monitoring
kubectl describe pod -n log-monitoring <pod-name>
kubectl logs -n log-monitoring deployment/devops-log-monitoring
kubectl get events -n log-monitoring --sort-by=.lastTimestamp
kubectl get endpoints -n log-monitoring devops-log-monitoring
```

- **Readiness** controls whether a pod should receive Service traffic.
- **Liveness** detects a container that should be restarted.
- Do not make liveness fail for every temporary dependency issue; that can create restart loops.
- The provided Prometheus scrape target is for Docker Compose. Kubernetes monitoring needs Kubernetes-aware discovery or an explicitly configured scrape target.

## 11. GitHub Actions

`.github/workflows/ci.yml` installs dependencies, runs `pytest`, and builds a Docker image on pushes and pull requests targeting `main`.

1. Create a GitHub repository and push this project to `main`.
2. Open the repository's **Actions** tab.
3. Inspect test and image-build logs.

The workflow does not push the image to a registry or deploy it. Add those stages only after configuring a registry and least-privilege secrets.

## 12. Terraform starter

This starter uses the **local provider** and creates a local file only; it does not create cloud resources or cloud charges.

```bash
cd terraform
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
terraform output
```

Review the plan before typing `yes`. Then clean up:

```bash
terraform destroy
```

For a real cloud project, design authentication, remote state, locking, permissions, cost controls and review gates before provisioning resources.

## 13. Troubleshooting

| Symptom | First checks |
|---|---|
| App will not start | `docker compose logs app`; check port 8080 |
| Import/dependency error | Activate `.venv`; reinstall requirements |
| Container exits | `docker ps -a`; `docker logs <container>` |
| Prometheus target down | **Status → Targets**; test `/metrics` |
| Empty Grafana panels | Generate requests; verify Prometheus data source |
| No Loki logs | `docker compose logs promtail loki`; inspect Docker socket permissions |
| Pod is not Ready | `kubectl describe pod`; check readiness and events |
| Service has no endpoints | Compare pod labels and Service selector; check readiness |
| `ImagePullBackOff` | Check image name, registry access or load image into cluster |
| `CrashLoopBackOff` | `kubectl logs --previous`; inspect exit reason and resource limits |
| CI fails | Reproduce with `pytest -q`; inspect the first failed assertion |

## 14. Production safety notes

This is a learning scaffold, not a production-ready observability platform. Before real deployment:

- Scan and update base images and dependencies.
- Keep credentials out of Git; use a secrets manager.
- Add TLS, authentication and network restrictions to monitoring tools.
- Configure storage, retention, backups and resource limits.
- Configure Alertmanager and tested notification routes.
- Review Kubernetes RBAC, security context, network policy and image provenance.
- Secure Terraform state and review plans before applying changes.
- Test failure scenarios in a non-production environment first.

## 15. Interview questions

**1. Readiness vs liveness?** Readiness controls traffic eligibility; liveness tells Kubernetes when a container should be restarted.

**2. Why can a pod be Running but users still see errors?** The app may not be ready, Service selectors may be wrong, endpoints may be empty, or ingress/network configuration may be broken.

**3. What does Prometheus do?** Scrapes and stores time-series metrics and evaluates alert rules.

**4. Why use Grafana?** It visualizes data from sources such as Prometheus and Loki.

**5. What does Loki do?** It stores and queries logs; Promtail forwards discovered container logs in this demo.

**6. Does an alert automatically fix the root cause?** No. An alert signals investigation. Remediation automation must be separately designed, constrained and tested.

**7. What should you check when a Service has no endpoints?** Pod labels, the Service selector, readiness status and namespace.

**8. What does the CI workflow do?** Installs dependencies, runs tests and verifies that the Docker image builds; it does not deploy the app.

---

<div align="center">

### 🚀 Learn • Build • Deploy • Monitor

**Follow [@the.devops111](https://www.instagram.com/the.devops111/) for practical DevOps projects and production scenarios.**

</div>
