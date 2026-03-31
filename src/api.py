from fastapi import FastAPI
from src.auth.controller import router as auth_router
from src.services.controller import router as service_router





#register all routes here
def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(service_router)