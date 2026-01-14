# FastAPI Observability Demo

This project demonstrates a FastAPI application instrumented with OpenTelemetry, supporting two visualization stacks: SigNoz and Grafana Stack.

## Features

- **FastAPI Application** with three endpoints:
  - `/fast`: Quick successful response
  - `/slow`: Response with 2-second delay
  - `/error`: Returns 500 status code and logs an error

- **OpenTelemetry Instrumentation**:
  - **Metrics**: Counter (request counts), Histogram (request latency), Gauge (live users)
  - **Traces**: Automatic instrumentation with custom spans
  - **Logs**: Structured logging with trace_id and span_id correlation

## Setup

### Prerequisites

- Python 3.8+
- Docker and Docker Compose

### Installation

1. Install Python dependencies:
```bash
pip install -r app/requirements.txt
```

## Running the Application

### Setup A: SigNoz

1. Start SigNoz stack:
```bash
docker-compose -f docker-compose.signoz.yml up -d
```

2. Run the application with SigNoz configuration:
```bash
export SETUP_TYPE=signoz
export OTLP_ENDPOINT=http://localhost:4317
uvicorn app.main:app --reload
```

3. Access SigNoz UI at: http://localhost:3301

### Setup B: Grafana Stack

1. Start Grafana stack (Prometheus, Tempo, Loki, Grafana):
```bash
docker-compose -f docker-compose.grafana.yml up -d
```

2. Run the application with Grafana configuration:
```bash
export SETUP_TYPE=grafana
export PROMETHEUS_PORT=9090
export TEMPO_ENDPOINT=http://localhost:4317
uvicorn app.main:app --reload
```

3. Access Grafana UI at: http://localhost:3000
   - Prometheus metrics endpoint: http://localhost:9090/metrics
   - Tempo traces: http://localhost:4317 (OTLP gRPC)
   - Loki logs: http://localhost:3100

## Environment Variables

- `SETUP_TYPE`: Either `signoz` or `grafana` (default: `signoz`)
- `OTLP_ENDPOINT`: OTLP endpoint URL (default: `http://localhost:4317`)
- `SERVICE_NAME`: Service name for telemetry (default: `fastapi-demo`)
- `PROMETHEUS_PORT`: Port for Prometheus metrics endpoint (default: `9090`)
- `TEMPO_ENDPOINT`: Tempo OTLP endpoint (default: `http://localhost:4317`)
- `LOKI_ENDPOINT`: Loki endpoint (default: `http://localhost:3100`)

## Testing the Endpoints

```bash
# Fast endpoint
curl http://localhost:8000/fast

# Slow endpoint (2 second delay)
curl http://localhost:8000/slow

# Error endpoint (500 status)
curl http://localhost:8000/error
```

## Metrics

The application exposes the following custom metrics:

- `http_requests_total`: Counter for total HTTP requests
- `http_request_duration_seconds`: Histogram for request latency
- `live_users`: UpDownCounter simulating live user count

## Traces

All requests are automatically traced with:
- Automatic FastAPI instrumentation
- Custom spans for each endpoint
- Span attributes for better filtering

## Logs

Logs are structured and automatically enriched with:
- `trace_id`: OpenTelemetry trace ID
- `span_id`: OpenTelemetry span ID

This enables correlation between logs, traces, and metrics.

