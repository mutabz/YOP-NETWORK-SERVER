# ==========================
# DATABASE
# ==========================
from app.core.db_imports import *  # noqa
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.api.v1 import v1_router

# ==========================
# EVENTS
# ==========================
from app.events.bootstrap import load_events


# ==========================
# APP STARTUP/SHUTDOWN
# ==========================
from app.core.startup import startup
from app.core.startup import shutdown
from app.core.realtime import manager
from app.core.realtime.registry import register_realtime_handlers
from app.core.realtime.heartbeat import HeartbeatService
from app.core.realtime import manager
from app.core.realtime.subscriber import subscriber




@asynccontextmanager
async def lifespan(app: FastAPI):
    # =====================================
    # LOAD ORM MODELS
    # ====================================
    # importing above automatically registers
    # all models into Base.metadata
    # =====================================
    # REGISTER EVENT HANDLERS
    # =====================================
    load_events()
    # =====================================
    # START SYSTEM SERVICES
    # =====================================
    await startup()
    print("🚀 ERP System Started")
    await subscriber.start()
    await manager.start()
    heartbeat = HeartbeatService( manager )
    await heartbeat.start()
    register_realtime_handlers()
    print("✅ WebSocket Manager Started")
    yield
    # =====================================
    # SHUTDOWN
    # =====================================
    await subscriber.stop()
    await heartbeat.stop()
    await manager.stop()
    await shutdown()
    print("🛑 ERP System Stopped")



app = FastAPI( title="ERP System", lifespan=lifespan )

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router( v1_router, prefix="/api/v1" )

