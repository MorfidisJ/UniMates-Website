from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from mangum import Mangum
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

import requests
import os


load_dotenv(".env")
app = FastAPI()

urlv3 = "https://api.convertkit.com/v3" 
urlv4 = "https://api.kit.com/v4" 
headers = {
    "X-Kit-Api-Key": os.getenv("API_KEY_V4")
}


class Subscriber(BaseModel):
    email: str
    first_name: Optional[str] = None


@app.get("/subscribers")
async def get_subscribers():
    response = requests.get(f"{urlv4}/subscribers", headers=headers)
    return {"subscriber_count": len(response.json()["subscribers"])}


@app.post("/subscribers")
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

handler = Mangum(app)

