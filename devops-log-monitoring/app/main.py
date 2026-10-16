import os, random
from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from app.health import health_bp
from app.logger import logger

REQUESTS = Counter("demo_http_requests_total", "HTTP requests handled", ["endpoint", "status"])

def create_app():
    app = Flask(__name__)
    app.config["SIMULATE_UNHEALTHY"] = False
    app.register_blueprint(health_bp)

    @app.after_request
    def count_request(response):
        REQUESTS.labels(request.endpoint or "unknown", str(response.status_code)).inc()
        return response

    @app.get("/")
    def index():
        logger.info("Application home endpoint requested")
        return jsonify(service="devops-log-monitoring", endpoints=[
            "/health/live", "/health/ready", "/metrics", "/simulate-error",
            "POST /simulate-failure", "POST /recover", "/demo/random-log"])

    @app.get("/work")
    def work():
        logger.info("Sample work completed")
        return jsonify(status="ok", result="sample work completed")

    @app.get("/simulate-error")
    def simulate_error():
        logger.error("Intentional demo HTTP 500")
        return jsonify(status="error", message="Intentional demo error"), 500

    @app.post("/simulate-failure")
    def simulate_failure():
        app.config["SIMULATE_UNHEALTHY"] = True
        logger.error("Failure simulation enabled; readiness now returns 503")
        return jsonify(status="failure_simulated"), 202

    @app.post("/recover")
    def recover():
        app.config["SIMULATE_UNHEALTHY"] = False
        logger.warning("Manual demo recovery completed")
        return jsonify(status="recovered"), 200

    @app.get("/demo/random-log")
    def random_log():
        level, message = random.choice([
            ("info", "Queue processed successfully"),
            ("warning", "Retrying transient dependency request"),
            ("error", "Simulated dependency timeout")])
        getattr(logger, level)(message)
        return jsonify(level=level, message=message)

    @app.get("/metrics")
    def metrics():
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
    return app

app = create_app()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
