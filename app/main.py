from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.jobs import router as jobs_router
from app.api.upload import router as upload_router
from app.core.logger import logger
from app.web.routes import router as web_router
from app.websocket.router import router as websocket_router


# ==========================================================
# Startup / Shutdown
# ==========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("=" * 70)
    logger.info("RDO Check AI iniciado.")
    logger.info("=" * 70)

    yield

    logger.info("=" * 70)
    logger.info("RDO Check AI finalizado.")
    logger.info("=" * 70)


# ==========================================================
# FastAPI
# ==========================================================

app = FastAPI(

    title="RDO Check AI",

    version="2.0.0",

    lifespan=lifespan,

    docs_url="/docs",

    redoc_url="/redoc"

)

# ==========================================================
# Middleware
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

# ==========================================================
# Arquivos Estáticos
# ==========================================================

app.mount(

    "/static",

    StaticFiles(directory="app/static"),

    name="static"

)

# ==========================================================
# Web
# ==========================================================

app.include_router(

    web_router

)

# ==========================================================
# API
# ==========================================================

app.include_router(

    upload_router,

    prefix="/api"

)

app.include_router(

    jobs_router,

    prefix="/api"

)

# ==========================================================
# WebSocket
# ==========================================================

app.include_router(

    websocket_router

)

# ==========================================================
# Health
# ==========================================================

@app.get("/health", tags=["System"])
async def health():

    return {

        "status": "online",

        "application": "RDO Check AI",

        "version": app.version

    }


@app.get("/ping", tags=["System"])
async def ping():

    return {

        "pong": True

    }