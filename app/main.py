from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import organization_controller, admin_controller
from app.utils.database import Database

app = FastAPI(
    title="Organization Management Service",
    description="Multi-tenant organization management system with MongoDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organization_controller.router)
app.include_router(admin_controller.router)

@app.on_event("startup")
async def startup_event():
    Database.get_client()

@app.on_event("shutdown")
async def shutdown_event():
    await Database.close()

@app.get("/")
async def root():
    return {
        "message": "Organization Management Service API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}