from flask import Blueprint, current_app, jsonify
health_bp = Blueprint("health", __name__)

@health_bp.get("/health/live")
def live():
    return jsonify(status="ok", check="live"), 200

@health_bp.get("/health/ready")
def ready():
    if current_app.config["SIMULATE_UNHEALTHY"]:
        return jsonify(status="not_ready"), 503
    return jsonify(status="ready"), 200
