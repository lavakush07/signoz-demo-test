# Quick Start Guide

## ✅ Setup Complete!

The FastAPI application is now ready to run. All dependencies are installed in a virtual environment.

## Running the Application

### Option 1: Using the Run Scripts (Recommended)

**For Grafana Stack:**
```bash
./run-grafana.sh
```

**For SigNoz:**
```bash
./run-signoz.sh
```

### Option 2: Manual Start

**For Grafana Stack:**
```bash
source venv/bin/activate
export SETUP_TYPE=grafana
export PROMETHEUS_PORT=9091
export TEMPO_ENDPOINT=http://localhost:4317
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**For SigNoz:**
```bash
source venv/bin/activate
export SETUP_TYPE=signoz
export OTLP_ENDPOINT=http://localhost:4319
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the Endpoints

Once the application is running, test the endpoints:

```bash
# Fast endpoint
curl http://localhost:8000/fast

# Slow endpoint (2 second delay)
curl http://localhost:8000/slow

# Error endpoint (returns 500)
curl http://localhost:8000/error
```

## Accessing Observability Data

### Grafana Stack:
- **Grafana UI**: http://localhost:3000
- **Prometheus Metrics**: http://localhost:9091/metrics (app metrics)
- **Prometheus Server**: http://localhost:9090 (scraping the app)
- **Tempo Traces**: http://localhost:4317 (OTLP gRPC)
- **Loki Logs**: http://localhost:3100

### SigNoz:
- **SigNoz UI**: http://localhost:3301
- **OTLP Endpoint**: http://localhost:4319 (gRPC), http://localhost:4320 (HTTP)

## Important Notes

1. **Virtual Environment**: Always activate the virtual environment first:
   ```bash
   source venv/bin/activate
   ```

2. **Port Conflicts**: 
   - The app runs on port 8000
   - Prometheus metrics endpoint is on port 9091 (to avoid conflict with Prometheus server on 9090)
   - Make sure the observability stacks are running before starting the app

3. **Grafana Stack**: Make sure it's running:
   ```bash
   docker-compose -f docker-compose.grafana.yml up -d
   ```

4. **SigNoz Stack**: Make sure it's running:
   ```bash
   docker-compose -f docker-compose.signoz.yml up -d
   ```

## Troubleshooting

If you get "Address already in use" errors:
- Check what's using the port: `lsof -i :8000` or `lsof -i :9091`
- Stop conflicting services or change the port in the environment variables

If imports fail:
- Make sure you've activated the virtual environment: `source venv/bin/activate`
- Verify dependencies: `pip list | grep fastapi`

