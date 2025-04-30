import time
from typing import Callable, Awaitable
from starlette.types import ASGIApp, Receive, Scope, Send
from prometheus_client import Counter, Histogram

liveness_requests_total = Counter(
    'liveness_requests_total', 'Total liveness requests', ['method', 'endpoint', 'status']
)
liveness_requests_success = Counter(
    'liveness_requests_success', 'Successful liveness responses', ['endpoint']
)
liveness_requests_error = Counter(
    'liveness_requests_error', 'Errored liveness responses', ['endpoint']
)
liveness_request_latency_seconds = Histogram(
    'liveness_request_latency_seconds', 'Request latency', ['endpoint']
)
liveness_inference_latency_seconds = Histogram(
    'liveness_inference_latency_seconds', 'Inference latency', ['endpoint']
)

class MetricsMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return
        method = scope['method']
        endpoint = scope['path']
        start_time = time.time()
        status_code_holder = {}
        inference_start = None
        inference_end = None

        async def custom_send(message):
            if message['type'] == 'http.response.start':
                status = message['status']
                status_code_holder['status'] = status
            await send(message)

        # Patch for inference timing
        scope['inference_timer'] = lambda: (inference_start, inference_end)
        try:
            await self.app(scope, receive, custom_send)
            status = status_code_holder.get('status', 500)
            liveness_requests_total.labels(method, endpoint, status).inc()
            if 200 <= status < 400:
                liveness_requests_success.labels(endpoint).inc()
            else:
                liveness_requests_error.labels(endpoint).inc()
        finally:
            elapsed = time.time() - start_time
            liveness_request_latency_seconds.labels(endpoint).observe(elapsed)
            if inference_start and inference_end:
                liveness_inference_latency_seconds.labels(endpoint).observe(inference_end - inference_start)
