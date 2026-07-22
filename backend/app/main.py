"""FastAPI 应用入口：CORS、路由挂载、初始化、可选托管前端产物。"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from . import seed
from .routers import companies, teams, resume, recruit, crawl

app = FastAPI(title="大厂情报站 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)
app.include_router(teams.router)
app.include_router(resume.router)
app.include_router(recruit.router)
app.include_router(crawl.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    seed.seed()


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "bigtech-intel"}


# 生产态：若已构建前端，则由后端直接托管（dev 用 Vite，不命中此分支）
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")
