from fastapi import APIRouter, HTTPException, status
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

# not dynamic but can save time on vercel
# resets on every sleep

_cache = set()

@api_router.get("/subscribers")
async def get_subscribers():
    global _cache

    if len(_cache) == 0:
        response = requests.get(f"{urlv4}/subscribers", headers={"X-Kit-Api-Key": os.getenv("API_KEY_V4")})
        if response.status_code >= 400:
            print(response.json()["errors"][0])
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
        
        subs = response.json()["subscribers"]
        _cache = set([record["email_address"] for record in subs])

    return {"subscriber_count": len(_cache)}


@api_router.post("/subscribers")
async def create_subscriber(sub: Subscriber):
    global _cache

    if sub.email == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No email provided")
    elif sub.email in _cache:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")

    # Create subscriber
    payload = {
        "email": sub.email,
        "first_name": sub.first_name,
        "form_id": os.getenv("FORM_ID"),
        "api_key": os.getenv("API_KEY_V3")
    }
    response = requests.post(f"{urlv3}/forms/{os.getenv('FORM_ID')}/subscribe", json=payload)

    if response.status_code >= 400:
        print(response.json())
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)

    _cache.add(sub.email)
    return JSONResponse(content={"subscriber": sub.model_dump()}, status_code=status.HTTP_201_CREATED)

