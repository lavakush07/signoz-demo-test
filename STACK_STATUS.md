# Stack Status

## ✅ Grafana Stack - RUNNING

All services are up and running:

- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Tempo**: http://localhost:4317 (gRPC), http://localhost:4318 (HTTP)
- **Loki**: http://localhost:3100

### To test with Grafana Stack:
```bash
./run-grafana.sh
# or
export SETUP_TYPE=grafana
uvicorn app.main:app --reload
```

## ⚠️ SigNoz Stack - Configuration Issue

SigNoz is having trouble connecting to ClickHouse. The infrastructure is running:
- ✅ ClickHouse: Running on port 9000
- ✅ Zookeeper: Running on port 2181
- ❌ SigNoz: Failing to connect to ClickHouse

### Current Issue:
SigNoz is trying to connect to `[::1]:9000` (localhost IPv6) instead of the `clickhouse` container hostname.

### Quick Test - Use Grafana Stack First:
Since Grafana stack is fully operational, you can test the application with it:

```bash
# Start the app with Grafana configuration
export SETUP_TYPE=grafana
export PROMETHEUS_PORT=9090
export TEMPO_ENDPOINT=http://localhost:4317
uvicorn app.main:app --reload

# Then test the endpoints:
curl http://localhost:8000/fast
curl http://localhost:8000/slow
curl http://localhost:8000/error

# View metrics in Prometheus:
# http://localhost:9090/metrics

# View traces in Grafana:
# http://localhost:3000 -> Explore -> Tempo
```

### SigNoz Alternative:
You can use the official SigNoz quickstart instead:
```bash
git clone https://github.com/SigNoz/signoz.git
cd signoz/deploy/docker/clickhouse-setup
docker-compose up -d
```

Then update the OTLP endpoint in your app to point to the official SigNoz instance.

