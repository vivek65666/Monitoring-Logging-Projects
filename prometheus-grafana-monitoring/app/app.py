import time
from flask import Flask, request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Define Prometheus Metrics
REQUEST_COUNT = Counter(
    'flask_http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'http_status']
)

REQUEST_LATENCY = Histogram(
    'flask_http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['endpoint']
)

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    if request.path == '/metrics':
        return response
        
    latency = time.time() - getattr(request, 'start_time', time.time())
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.path,
        http_status=response.status_code
    ).inc()
    
    REQUEST_LATENCY.labels(endpoint=request.path).observe(latency)
    
    return response

@app.route('/')
def home():
    return "Hello from the monitored Flask app!"

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)