import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from typing import Any, Callable

try:
    from multiprocessing import cpu_count
except ImportError:
    def cpu_count():
        return 4

from app.config.settings import settings

# ThreadPoolExecutor shared at module level
MAX_WORKERS = int(os.getenv("MAX_WORKERS") or getattr(settings, "MAX_WORKERS", None) or cpu_count())
_executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

def get_executor():
    return _executor

async def run_in_thread(func: Callable, *args, **kwargs) -> Any:
    """
    Run a sync function in the shared thread-pool executor.
    Returns the result as an awaitable coroutine.
    """
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, lambda: func(*args, **kwargs))

def shutdown_executor():
    _executor.shutdown(wait=True)
