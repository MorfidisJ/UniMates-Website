import json
import os
import csv
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'matching_config.json')
USERS_PATH = os.path.join(os.path.dirname(__file__), 'users_db.json')  # You may need to adjust this if you use a DB
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), 'feedback_export.csv')

# Load feedback history
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
feedback_history = config.get('feedback_history', [])

# Load users_db (assume you have a JSON dump; otherwise, adapt to your DB)
with open(USERS_PATH, 'r') as f:
    users_db = json.load(f)

def get_similarities(user1, user2):
    cats = ["personality_score", "habit_score", "lifestyle_score", "characteristic_score"]
    similarities = {}
    for cat in cats:
        t1 = user1.get(cat, {})
        t2 = user2.get(cat, {})
        all_traits = set(t1.keys()) | set(t2.keys())
        for trait in all_traits:
            val1 = t1.get(trait, 0)
            val2 = t2.get(trait, 0)
            similarities[f'{cat}_{trait}'] = 1 - abs(val1 - val2) / (2 * max(abs(val1), abs(val2), 1))
    return similarities

with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    fieldnames = ['user_id', 'other_user_id', 'rating', 'timestamp']
    # Add all possible trait similarity columns
    all_traits = set()
    for user in users_db.values():
        for cat in ["personality_score", "habit_score", "lifestyle_score", "characteristic_score"]:
            all_traits.update([f'{cat}_{t}' for t in user.get(cat, {})])
    fieldnames += sorted(list(all_traits))
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for fb in feedback_history:
        u1 = users_db.get(fb['user_id'])
        u2 = users_db.get(fb['other_user_id'])
        if not u1 or not u2:
            continue
        row = {
            'user_id': fb['user_id'],
            'other_user_id': fb['other_user_id'],
            'rating': fb['rating'],
            'timestamp': fb['timestamp']
        }
        row.update(get_similarities(u1, u2))
        writer.writerow(row)
print(f'Exported feedback data to {OUTPUT_CSV}') 