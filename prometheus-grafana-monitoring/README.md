# Flask Observability & Monitoring Suite

A production-grade monitoring and observability pipeline built for Flask applications using **Prometheus** and **Grafana**. This project demonstrates containerized metrics collection, real-time scraping, custom PromQL querying, and visual dashboard design.

---

## 🚀 Architecture & Data Flow

```text
+-------------------------------------------------------------------+
|                         Local Environment                         |
|                                                                   |
|   +-------------------+                     +-----------------+   |
|   |     Flask App     | --- exposes metrics |   Prometheus    |   |
|   | (Port 5000 /metrics) | <---------------- | (Port 9090)     |   |
|   +-------------------+    scrapes via HTTP +-----------------+   |
|                                                      |            |
|                                                      | queries    |
|                                                      v            |
|                                             +-----------------+   |
|                                             |     Grafana     |   |
|                                             | (Port 3000)     |   |
|                                             +-----------------+   |
+-------------------------------------------------------------------+
Instrumentation: The Flask application uses prometheus-client to expose custom HTTP metrics (flask_http_requests_total) on its /metrics endpoint.

Scraping: Prometheus periodically scrapes the Flask application container to ingest time-series data via HTTP.

Visualization: Grafana connects as a data source to Prometheus, utilizing custom PromQL queries (rate(), error filtering via regex for 4xx/5xx/404) to render real-time traffic and error rate graphs.

📊 Grafana Dashboards
Our monitoring suite features real-time panels tracking application performance:

Flask Request Rate: Monitors incoming HTTP request distribution across methods and endpoints (/, static files, etc.).

Flask Error Rate: Filters and visualizes HTTP status codes to instantly flag client or server errors.

Dashboard Preview
🛠️ Tech Stack
Backend: Python, Flask

Metrics & Monitoring: Prometheus (prometheus-client)

Visualization: Grafana

Containerization: Docker / Docker Compose

⚙️ Getting Started & Local Setup
1. Clone the Repository
Bash
git clone [https://github.com/vivek65666/Monitoring-Logging-Projects.git](https://github.com/vivek65666/Monitoring-Logging-Projects.git)
cd Monitoring-Logging-Projects/prometheus-grafana-monitoring
2. Run with Docker Compose
Spin up the Flask application, Prometheus, and Grafana containers simultaneously:

Bash
docker-compose up -d
3. Access the Services
Flask Application: http://localhost:5000

Prometheus UI: http://localhost:9090 (Verify targets at /targets)

Grafana Dashboard: http://localhost:3000 (Default credentials: admin / admin)


---

### How to save and push this:
1. Create a file named `README.md` inside your `prometheus-grafana-monitoring` folder and paste the code above.
2. Run these commands in your terminal to update GitHub:
   ```bash
   git add README.md
   git commit -m "Add full professional README.md"
   git push
