from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from dotenv import load_dotenv, find_dotenv
from api.api import api_router

import os

# load .env on dev only
if os.getenv("VERCEL") is None:
    dotenv_path = find_dotenv()
    print("loading environment from:", dotenv_path)
    load_dotenv(dotenv_path)

app = FastAPI()

origins = [
    "https://landing-page-unimatesnet.vercel.app",
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

