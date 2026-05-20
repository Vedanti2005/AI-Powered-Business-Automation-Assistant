from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import connect_db, close_db
from routers import chat, leads, dashboard, automation


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Codenixia AI Business Automation Assistant",
    description="AI-powered business assistant with lead management, chatbot, and automation workflows.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/chat", tags=["AI Chatbot"])
app.include_router(leads.router, prefix="/api/leads", tags=["Lead Management"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(automation.router, prefix="/api/automation", tags=["Automation"])


@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "running",
        "message": "Codenixia AI Business Automation Assistant API",
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "service": "codenixia-backend"}
