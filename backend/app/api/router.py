from fastapi import APIRouter

from app.api.routes import documents, health, verification

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(
    verification.router,
    prefix="/verification",
    tags=["verification"],
)
