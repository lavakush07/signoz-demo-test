#!/bin/bash
# Script to run the FastAPI app with Grafana Stack configuration

# Activate virtual environment
source venv/bin/activate

export SETUP_TYPE=grafana
export PROMETHEUS_PORT=9091
export TEMPO_ENDPOINT=http://localhost:4317
export SERVICE_NAME=fastapi-demo

echo "Starting FastAPI app with Grafana Stack configuration..."
echo "Prometheus metrics port: $PROMETHEUS_PORT"
echo "Tempo endpoint: $TEMPO_ENDPOINT"
echo ""
echo "Make sure Grafana Stack is running:"
echo "  docker-compose -f docker-compose.grafana.yml up -d"
echo ""
echo "Access Grafana UI at: http://localhost:3000"
echo "Prometheus metrics at: http://localhost:9090/metrics"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

