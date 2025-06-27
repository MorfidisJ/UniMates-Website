import joblib
import os
import numpy as np
import json

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'match_model.pkl')
USERS_PATH = os.path.join(os.path.dirname(__file__), 'users_db.json')

model = joblib.load(MODEL_PATH)

# Load users_db for feature computation (or pass users as needed)
with open(USERS_PATH, 'r') as f:
    users_db = json.load(f)

def compute_features(user1, user2):
    cats = ["personality_score", "habit_score", "lifestyle_score", "characteristic_score"]
    features = []
    for cat in cats:
        t1 = user1.get(cat, {})
        t2 = user2.get(cat, {})
        all_traits = set(t1.keys()) | set(t2.keys())
        for trait in sorted(all_traits):
            val1 = t1.get(trait, 0)
            val2 = t2.get(trait, 0)
            features.append(1 - abs(val1 - val2) / (2 * max(abs(val1), abs(val2), 1)))
    return np.array(features).reshape(1, -1)

def predict_match(user_id, other_user_id):
    u1 = users_db.get(user_id)
    u2 = users_db.get(other_user_id)
    if not u1 or not u2:
        return None
    feats = compute_features(u1, u2)
    return float(model.predict(feats)[0]) 