"""
OpenTelemetry instrumentation setup for the FastAPI application.
Supports both SigNoz (OTLP) and Grafana Stack (Prometheus/Tempo/Loki) configurations.
"""
import os
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server

# Setup type: "signoz" or "grafana"
SETUP_TYPE = os.getenv("SETUP_TYPE", "signoz")

# OTLP Configuration (for SigNoz)
# Note: Using port 4319 to avoid conflict with Tempo (which uses 4317)
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://localhost:4319")
SERVICE_NAME = os.getenv("SERVICE_NAME", "fastapi-demo")

# Prometheus Configuration (for Grafana Stack)
# Using 9091 to avoid conflict with Prometheus server (which uses 9090)
PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "9091"))

# Tempo Configuration (for Grafana Stack)
TEMPO_ENDPOINT = os.getenv("TEMPO_ENDPOINT", "http://localhost:4317")

# Loki Configuration (for Grafana Stack) - handled via logging exporter
LOKI_ENDPOINT = os.getenv("LOKI_ENDPOINT", "http://localhost:3100")

logger = logging.getLogger(__name__)


def setup_instrumentation(app):
    """Initialize OpenTelemetry instrumentation based on setup type."""
    
    # Create resource with service name
    resource = Resource.create({
        "service.name": SERVICE_NAME,
        "service.version": "1.0.0",
    })
    
    # Setup Traces
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)
    
    if SETUP_TYPE == "signoz":
        # SigNoz Setup: Use OTLP for both traces and metrics
        logger.info(f"Setting up SigNoz instrumentation (OTLP: {OTLP_ENDPOINT})")
        
        # Trace exporter (OTLP)
        trace_exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True)
        trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
        
        # Metrics exporter (OTLP)
        metric_exporter = OTLPMetricExporter(endpoint=OTLP_ENDPOINT, insecure=True)
        metric_reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5000)
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[metric_reader]))
        
    else:  # grafana
        # Grafana Stack Setup: Prometheus for metrics, OTLP for traces (Tempo)
        logger.info(f"Setting up Grafana Stack instrumentation")
        logger.info(f"  - Prometheus metrics on port {PROMETHEUS_PORT}")
        logger.info(f"  - Tempo traces: {TEMPO_ENDPOINT}")
        
        # Trace exporter (OTLP to Tempo)
        trace_exporter = OTLPSpanExporter(endpoint=TEMPO_ENDPOINT, insecure=True)
        trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
        
        # Metrics exporter (Prometheus)
        prometheus_reader = PrometheusMetricReader()
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[prometheus_reader]))
        
        # Start Prometheus metrics endpoint
        start_http_server(PROMETHEUS_PORT)
        logger.info(f"Prometheus metrics available at http://localhost:{PROMETHEUS_PORT}/metrics")
    
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    # Instrument logging (for trace_id/span_id correlation)
    LoggingInstrumentor().instrument(set_logging_format=True)
    
    logger.info("OpenTelemetry instrumentation completed")


def get_meter():
    """Get the meter for creating custom metrics."""
    return metrics.get_meter(__name__)


def get_tracer():
    """Get the tracer for creating custom spans."""
    return trace.get_tracer(__name__)

