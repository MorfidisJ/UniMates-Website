from fastapi import APIRouter, HTTPException
import json
import os
from datetime import datetime

TRAIT_FEEDBACK_PATH = os.path.join(os.path.dirname(__file__), 'trait_feedback.json')
router = APIRouter()

def load_trait_feedback():
    if os.path.exists(TRAIT_FEEDBACK_PATH):
        with open(TRAIT_FEEDBACK_PATH, 'r') as f:
            return json.load(f)
    return []

def save_trait_feedback(feedback):
    with open(TRAIT_FEEDBACK_PATH, 'w') as f:
        json.dump(feedback, f, indent=2)

@router.post('/trait-feedback')
async def submit_trait_feedback(user_id: str, other_user_id: str, trait: str, rating: float):
    if not 0 <= rating <= 1:
        raise HTTPException(status_code=400, detail='Rating must be between 0 and 1')
    feedback = load_trait_feedback()
    feedback.append({
        'user_id': user_id,
        'other_user_id': other_user_id,
        'trait': trait,
        'rating': rating,
        'timestamp': datetime.utcnow().isoformat()
    })
    save_trait_feedback(feedback)
    return {'message': 'Trait feedback submitted'} 