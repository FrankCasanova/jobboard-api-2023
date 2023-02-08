from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from core.config import settings
from apis.base import api_router
from db.session import engine   #new
from db.base_class import Base  #new


def include_router(app) -> None:
	app.include_router(api_router)


def configure_static(app) -> None:
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables() -> None:
    print('Creating tables.')
    Base.metadata.create_all(bind=engine)

	
def start_application() -> FastAPI():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	include_router(app)
	configure_static(app)
	create_tables()       
	return app

app = start_application()



