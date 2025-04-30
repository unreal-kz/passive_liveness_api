import os
from typing import Callable, Awaitable
from starlette.types import ASGIApp, Receive, Scope, Send

class TracingMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app
        self.tracer = None
        self.enabled = os.getenv('ENABLE_TRACING', 'true').lower() == 'true'
        self._init_tracer()

    def _init_tracer(self):
        if not self.enabled:
            return
        try:
            from opentelemetry import trace
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            endpoint = os.getenv('OTEL_EXPORTER_OTLP_ENDPOINT', 'http://localhost:4318')
            resource = Resource.create({"service.name": "passive-liveness-api"})
            provider = TracerProvider(resource=resource)
            processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer(__name__)
        except ImportError:
            self.enabled = False
            self.tracer = None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if not self.enabled or scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        tracer = self.tracer
        with tracer.start_as_current_span('http.request', attributes={"http.target": scope['path']}) as span:
            # Optionally, add more request attributes here
            async def inference_timer():
                with tracer.start_as_current_span('liveness.inference'):
                    pass  # This is a hook for business logic to time inference
            scope['inference_timer'] = inference_timer
            await self.app(scope, receive, send)
