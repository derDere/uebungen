from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import tools, checklists, templates, export
from . import seed_data

app = FastAPI(title="Tool Helper API", version="1.0.0")

# CORS configuration for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tools.router)
app.include_router(checklists.router)
app.include_router(templates.router)
app.include_router(export.router)


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
    seed_data.seed_database()


@app.get("/")
def root():
    return {"message": "Tool Helper API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
