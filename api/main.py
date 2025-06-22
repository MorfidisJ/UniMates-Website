from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv
from api  import api_router

load_dotenv("../.env")
app = FastAPI()

origins = [
    "http://localhost:8000",
    "https://unimates.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api")
app.mount("/", StaticFiles(directory="../static", html=True), name="static")

