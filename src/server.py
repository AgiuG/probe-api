from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.controller import router

def init_routers(app: FastAPI):
  app.include_router(router)

def create_app() -> FastAPI:
  app = FastAPI(
    title="FastAPI Sondas",
    description="FastAPI Sondas",
    version="1.0.0",
  )
  
  init_routers(app)
  return app

app = create_app()