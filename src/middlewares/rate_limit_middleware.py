from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse  # Importar JSONResponse
from time import time
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds 
        self.ip_request_times = defaultdict(list)
        
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time()
        
        request_times = self.ip_request_times[client_ip]
        self.ip_request_times[client_ip] = [t for t in request_times if t > current_time - self.window_seconds]
 
        if len(self.ip_request_times[client_ip]) >= self.max_requests:
            return JSONResponse(status_code=429, content=[
            {
                "loc": ["rate"],
                "msg": "Too many requests in a short amount of time. Please try again later.",
                "type": "rate limit"
            }
        ])

        self.ip_request_times[client_ip].append(current_time)

        response = await call_next(request)
        return response


