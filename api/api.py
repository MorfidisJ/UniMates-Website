from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from pydantic import BaseModel
from typing import Optional, List

import gspread
import requests
import base64
import json
import os


# Subscribers and Kit

urlv3 = "https://api.convertkit.com/v3" 
urlv4 = "https://api.kit.com/v4" 

class Subscriber(BaseModel):
    email: str
    first_name: Optional[str] = None


# Sheets

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

gc = gspread.service_account_from_dict(json.loads(base64.b64decode(os.getenv("GOOGLE_CREDENTIALS"))))
sheets = gc.open_by_key(os.getenv("SPREADSHEET_KEY"))
print(sheets)
quiz_sheet = gc.open_by_key(os.getenv("SPREADSHEET_KEY")).sheet1
matcher_sheet = gc.open_by_key(os.getenv("SPREADSHEET_KEY")).get_worksheet(1)

class QuizResult(BaseModel):
    email: str
    personalityType: str
    compatibleType: str

class QuizWMatch(BaseModel):
    email: str
    name: str
    phone: str
    gender: str
    city: str
    answers: List[int]

# API Router

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
            print(response.status_code)
            print(response.text)
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)
        
        subs = response.json()["subscribers"]
        _cache = set([record["email_address"] for record in subs])

    print(_cache)
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

    print("Reseponse:", response.status_code)
    if response.status_code >= 400:
        print(response.json())
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)

    print(sub.email, "subscribed")
    _cache.add(sub.email)
    return JSONResponse(content={"subscriber": sub.dict()}, status_code=status.HTTP_201_CREATED)



@api_router.post("/compatible-choice")
async def quiz_result(res: QuizResult):
    quiz_sheet.append_row([res.email, res.personalityType, res.compatibleType])

@api_router.post("/quiz-with-match")
async def store_matching_quiz_result(res: QuizWMatch):
    # send the quiz responses to matcher sheet
    matcher_sheet.append_row([res.name, res.email, res.city, res.phone, res.gender] + res.answers)
    return {"status": "created"}   
