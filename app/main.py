from fastapi import FastAPI
from app.api import routes
from  fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origin = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes.router)