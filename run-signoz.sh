#!/bin/bash
# Script to run the FastAPI app with SigNoz configuration

# Activate virtual environment
source venv/bin/activate

export SETUP_TYPE=signoz
export OTLP_ENDPOINT=http://localhost:4319
export SERVICE_NAME=fastapi-demo

echo "Starting FastAPI app with SigNoz configuration..."
echo "OTLP Endpoint: $OTLP_ENDPOINT"
echo ""
echo "Make sure SigNoz is running:"
echo "  docker-compose -f docker-compose.signoz.yml up -d"
echo ""
echo "Access SigNoz UI at: http://localhost:3301"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

