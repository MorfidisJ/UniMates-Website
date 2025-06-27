import math
from datetime import datetime

def exponential_decay(value, timestamp, now=None, half_life_days=90):
    if now is None:
        now = datetime.utcnow()
    dt = now - datetime.fromisoformat(timestamp)
    days = dt.total_seconds() / (3600*24)
    decay = 0.5 ** (days / half_life_days)
    return value * decay

def apply_time_weighted_answers(user_responses):
    now = datetime.utcnow()
    weighted = {}
    for resp in user_responses:
        val = resp['answer']
        ts = resp.get('timestamp', now.isoformat())
        weighted[resp['question_id']] = exponential_decay(val, ts, now)
    return weighted 