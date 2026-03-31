from fastapi import FastAPI
from .database.core import Base, engine
from .api import register_routes
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=['*'],
    allow_methods=['*']
)



Base.metadata.create_all(bind=engine)

register_routes(app=app)