import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.middleware.error_handler import error_handler_middleware
from api.middleware.logging import logging_middleware
from api.middleware.rate_limit import rate_limit_middleware
from api.routes import analytics, auth, chat, products, research, saved
from config import get_settings
from database.connection import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="AI Shopping Assistant API",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(logging_middleware)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(error_handler_middleware)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(saved.router, prefix="/api/v1/saved", tags=["Saved Products"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(research.router, prefix="/api/v1/research", tags=["Research"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}


static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")


@app.get("/")
async def root():
    return FileResponse(os.path.join(static_dir, "chat.html"))


@app.get("/chat")
async def chat_ui():
    return FileResponse(os.path.join(static_dir, "chat.html"))
