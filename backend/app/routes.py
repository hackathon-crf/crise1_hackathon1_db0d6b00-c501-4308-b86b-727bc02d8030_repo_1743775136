from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from backend.app.services import test_service
from settings.config import settings


app_router = APIRouter(
    prefix="/api/app",
    tags=["Retrieval QA"],
)

def create_app(root_path: str = "") -> FastAPI:
    """
    Creating a FastAPI instance and registering routes.

    Args:
        root_path: The root path where the API is mounted (e.g., /username/app_name)
    """

    backend_app = FastAPI(
        title="Template App",
        version="1.0.0",
        openapi_version="3.1.0",
        root_path=root_path
    )

    # CORS Configuration
    backend_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # Registering routes
    backend_app.include_router(app_router)
    return backend_app

@app_router.get("/test/")
async def test():
        return {
            "status:": 200,
            "message": test_service()
        }


    # Registering routes
