# import uvicorn
from apis.base import api_router
from core.config import settings
from db.base_class import Base
from db.session import engine
from db.utils import check_db_connected
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.staticfiles import StaticFiles
from webapps.base import api_router as web_app_router


origins = [
    "https://jobboard-api-2023-production.up.railway.app/",
]


def include_router(app) -> None:
    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app) -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def start_application() -> FastAPI():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(HTTPSRedirectMiddleware)


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
