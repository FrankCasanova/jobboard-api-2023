import uvicorn
from contextlib import asynccontextmanager
from apis.base import api_router
from core.config import settings
from db.base_class import Base
from db.session import engine
from db.utils import check_db_connected
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from webapps.base import api_router as web_app_router

# origins = [
#     "https://jobboard-api-2023-production.up.railway.app/",
# ]

def include_router(app) -> None:
    app.include_router(api_router)
    app.include_router(web_app_router)

def configure_static(app) -> None:
    app.mount("/static", StaticFiles(directory="backend/static"), name="static")

def create_tables() -> None:
    Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await check_db_connected()
    yield
    # Shutdown
    # Add any cleanup code here if needed

def start_application() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        lifespan=lifespan
    )
    include_router(app)
    configure_static(app)
    create_tables()
    return app

app = start_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)