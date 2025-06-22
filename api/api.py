from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional

import requests
import os

urlv3 = "https://api.convertkit.com/v3" 
urlv4 = "https://api.kit.com/v4" 

class Subscriber(BaseModel):
    email: str
    first_name: Optional[str] = None

api_router = APIRouter()

@api_router.get("/subscribers")
async def get_subscribers():
    response = requests.get(f"{urlv4}/subscribers", headers={"X-Kit-Api-Key": os.getenv("API_KEY_V4")})
    return {"subscriber_count": len(response.json()["subscribers"])}


@api_router.post("/subscribers")
async def create_subscriber(sub: Subscriber):
    if sub.email == "":
        raise HTTPException(status_code=400, detail="No email provided")

    # Create subscriber
    payload = {
        "email": sub.email,
        "first_name": sub.first_name,
        "form_id": os.getenv("FORM_ID"),
        "api_key": os.getenv("API_KEY_V3")
    }
    response = requests.post(f"{urlv3}/forms/{os.getenv('FORM_ID')}/subscribe", json=payload)
    return JSONResponse(content={"subscriber": sub}, status_code=201)

