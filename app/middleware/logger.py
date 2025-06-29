#logs api tracks
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import os


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/api_activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)

class APILoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        method = request.method
        path = request.url.path
        query = request.url.query

        log_msg = f"{ip} {method} {path}" + (f"?{query}" if query else "")
        logging.info(log_msg)

        response = await call_next(request)
        return response

