from fastapi import FastAPI, HTTPException, Request
import time
import logging
import random
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from app.instrumentation import setup_instrumentation, get_meter, get_tracer

app = FastAPI()

# Configure structured logging - OpenTelemetry will inject trace_id and span_id

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize instrumentation
setup_instrumentation(app)


meter = get_meter()
tracer = get_tracer()

# Create custom metrics
request_counter = meter.create_counter(
    name="http_requests_total",
    description="Total number of HTTP requests",
    unit="1"
)

request_latency = meter.create_histogram(
    name="http_request_duration_seconds",
    description="HTTP request latency in seconds",
    unit="s"
)

live_users_gauge = meter.create_up_down_counter(
    name="live_users",
    description="Number of live users (simulated)",
    unit="1"
)


current_users = 0


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect metrics and add trace context to logs."""
    start_time = time.time()
    path = request.url.path
    
    
    request_counter.add(1, {"method": request.method, "path": path})
    
    
    global current_users
    if random.random() > 0.7:  # 30% chance
        current_users += random.randint(1, 3)
        live_users_gauge.add(random.randint(1, 3))
    elif random.random() > 0.5 and current_users > 0:  # 20% chance if users exist
        decrement = random.randint(1, min(2, current_users))
        current_users -= decrement
        live_users_gauge.add(-decrement)
    
    try:
        response = await call_next(request)
        status_code = response.status_code
        
        # Record latency
        duration = time.time() - start_time
        request_latency.record(duration, {"method": request.method, "path": path, "status": str(status_code)})
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        request_latency.record(duration, {"method": request.method, "path": path, "status": "500"})
        raise
        
## Functions for fast, slow and error 

@app.get("/fast")
def fast():
    """Fast endpoint - quick successful response."""
    with tracer.start_as_current_span("fast_endpoint") as span:
        span.set_attribute("endpoint", "/fast")
        span.set_attribute("response_time", "fast")
        
        logger.info("Processing fast request")
        return {"message": "fast response"}


@app.get("/slow")
def slow():
    """Slow endpoint - response with 2-second delay."""
    with tracer.start_as_current_span("slow_endpoint") as span:
        span.set_attribute("endpoint", "/slow")
        span.set_attribute("delay_seconds", 2)
        
        logger.info("Processing slow request - will delay 2 seconds")
        time.sleep(2)
        
        span.set_attribute("completed", True)
        logger.info("Slow request completed")
        return {"message": "slow response"}


@app.get("/error")
def error():
    """Error endpoint - returns 500 status code and logs an error."""
    with tracer.start_as_current_span("error_endpoint") as span:
        span.set_attribute("endpoint", "/error")
        span.set_status(Status(StatusCode.ERROR, "Intentional error for testing"))
        
        error_msg = "Something went wrong! This is a test error."
        logger.error(error_msg, extra={"error_type": "test_error", "endpoint": "/error"})
        
        raise HTTPException(status_code=500, detail="Internal server error")
