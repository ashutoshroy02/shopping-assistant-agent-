import time
from collections import defaultdict

from fastapi import Request
from fastapi.responses import JSONResponse

rate_limit_store: dict[str, list[float]] = defaultdict(list)

RATE_LIMITS = {
    "/api/v1/auth/register": (10, 60),
    "/api/v1/auth/login": (10, 60),
    "/api/v1/auth/refresh": (10, 60),
    "/api/v1/chat": (30, 60),
    "/api/v1/products/recommend": (20, 60),
    "/api/v1/products/compare": (20, 60),
    "/api/v1/products/track-price": (10, 60),
    "/api/v1/products/price-history": (20, 60),
    "/api/v1/research": (5, 60),
    "/api/v1/analytics": (60, 60),
}


async def rate_limit_middleware(request: Request, call_next):
    path = request.url.path
    client_ip = request.client.host if request.client else "unknown"
    key = f"{client_ip}:{path}"

    if path in RATE_LIMITS:
        max_requests, window = RATE_LIMITS[path]
        now = time.time()

        rate_limit_store[key] = [
            t for t in rate_limit_store[key] if now - t < window
        ]

        if len(rate_limit_store[key]) >= max_requests:
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many requests. Please try again later.",
                    }
                },
                headers={"Retry-After": str(window)},
            )

        rate_limit_store[key].append(now)

    response = await call_next(request)
    return response



