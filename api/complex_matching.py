from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional, Any
import json
import uuid
from datetime import datetime
import asyncio
from enum import Enum
import math
from fastapi.middleware.cors import CORSMiddleware
import os
import json as _json

app = FastAPI(title="UniMates Complex Matching API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. For production, specify your domain.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data Models
class QuestionType(str, Enum):
    PERSONALITY = "personality"
    HABIT = "habit"
    LIFESTYLE = "lifestyle"
    CHARACTERISTIC = "characteristic"
    PREFERENCE = "preference"

class QuestionCategory(str, Enum):
    STUDY_HABITS = "study_habits"
    SOCIAL_PREFERENCES = "social_preferences"
    SLEEP_SCHEDULE = "sleep_schedule"
    CLEANLINESS = "cleanliness"
    NOISE_TOLERANCE = "noise_tolerance"
    GUEST_PREFERENCES = "guest_preferences"
    FINANCIAL_ATTITUDE = "financial_attitude"
    COMMUNICATION_STYLE = "communication_style"
    CONFLICT_RESOLUTION = "conflict_resolution"
    PERSONAL_SPACE = "personal_space"
    LIFESTYLE = "lifestyle"

class Question(BaseModel):
    id: str
    text: str
    category: QuestionCategory
    type: QuestionType
    weight: float = 1.0
    options: List[Dict[str, Any]]
    required: bool = True

class UserResponse(BaseModel):
    question_id: str
    answer: Any
    confidence: float = 1.0

class UserProfile(BaseModel):
    user_id: str
    email: EmailStr
    responses: List[UserResponse]
    personality_score: Dict[str, float] = {}
    habit_score: Dict[str, float] = {}
    lifestyle_score: Dict[str, float] = {}
    characteristic_score: Dict[str, float] = {}
    elo_rating: float = 1200.0
    created_at: datetime
    updated_at: datetime

class MatchRequest(BaseModel):
    user_id: str
    preferences: Dict[str, Any] = {}
    max_matches: int = 5

class MatchResult(BaseModel):
    user_id: str
    email: str
    compatibility_score: float
    personality_match: float
    habit_match: float
    lifestyle_match: float
    characteristic_match: float
    common_traits: List[str]
    potential_conflicts: List[str]

class SubmitProfileRequest(BaseModel):
    email: EmailStr
    responses: List[UserResponse]

# In-memory storage (replace with database in production)
users_db: Dict[str, UserProfile] = {}
questions_db: List[Question] = []

# --- Dynamic config loading ---
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'matching_config.json')
def load_matching_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return _json.load(f)
    return {
        "category_weights": {
            "personality": 0.3,
            "habit": 0.25,
            "lifestyle": 0.25,
            "characteristic": 0.2
        },
        "trait_weights": {},
        "similarity_method": "cosine"
    }
matching_config = load_matching_config()

# --- Population averages for missing data imputation ---
def get_population_trait_averages():
    trait_sums = {}
    trait_counts = {}
    for user in users_db.values():
        for cat in ["personality_score", "habit_score", "lifestyle_score", "characteristic_score"]:
            for trait, val in getattr(user, cat, {}).items():
                trait_sums[trait] = trait_sums.get(trait, 0) + val
                trait_counts[trait] = trait_counts.get(trait, 0) + 1
    return {trait: trait_sums[trait]/trait_counts[trait] for trait in trait_sums if trait_counts[trait] > 0}

# --- Advanced Similarity Metrics ---
def pearson_similarity(v1, v2):
    n = len(v1)
    if n == 0:
        return 0.5
    mean1 = sum(v1) / n
    mean2 = sum(v2) / n
    num = sum((a - mean1) * (b - mean2) for a, b in zip(v1, v2))
    den1 = math.sqrt(sum((a - mean1) ** 2 for a in v1))
    den2 = math.sqrt(sum((b - mean2) ** 2 for b in v2))
    if den1 * den2 == 0:
        return 0.5
    return 0.5 + 0.5 * (num / (den1 * den2))

def jaccard_similarity(v1, v2):
    set1 = set([i for i, v in enumerate(v1) if v > 0])
    set2 = set([i for i, v in enumerate(v2) if v > 0])
    if not set1 and not set2:
        return 1.0
    return len(set1 & set2) / len(set1 | set2)

# --- Cluster-based imputation ---
def get_cluster_trait_averages(target_user, k=5):
    # Find k most similar users (cosine) and average their traits
    similarities = []
    for user in users_db.values():
        if user.user_id == target_user.user_id:
            continue
        sim = 0
        for cat in ["personality_score", "habit_score", "lifestyle_score", "characteristic_score"]:
            sim += calculate_trait_similarity_dynamic(getattr(target_user, cat), getattr(user, cat))
        similarities.append((sim, user))
    similarities.sort(reverse=True, key=lambda x: x[0])
    top_users = [u for _, u in similarities[:k]]
    trait_sums = {}
    trait_counts = {}
    for user in top_users:
        for cat in ["personality_score", "habit_score", "lifestyle_score", "characteristic_score"]:
            for trait, val in getattr(user, cat, {}).items():
                trait_sums[trait] = trait_sums.get(trait, 0) + val
                trait_counts[trait] = trait_counts.get(trait, 0) + 1
    return {trait: trait_sums[trait]/trait_counts[trait] for trait in trait_sums if trait_counts[trait] > 0}

# --- Use trait weights in similarity calculation ---
def calculate_trait_similarity_dynamic(traits1, traits2, method=None, trait_weights=None, impute_user=None):
    if method is None:
        method = matching_config.get("similarity_method", "cosine")
    all_traits = set(traits1.keys()) | set(traits2.keys())
    if impute_user is not None:
        pop_avg = get_cluster_trait_averages(impute_user)
    else:
        pop_avg = get_population_trait_averages()
    v1 = [(traits1.get(t, pop_avg.get(t, 0))) for t in all_traits]
    v2 = [(traits2.get(t, pop_avg.get(t, 0))) for t in all_traits]
    weights = [trait_weights.get(t, 1.0) if trait_weights else 1.0 for t in all_traits]
    if method == "cosine":
        dot = sum(a*b*w for a, b, w in zip(v1, v2, weights))
        norm1 = math.sqrt(sum((a*w)**2 for a, w in zip(v1, weights)))
        norm2 = math.sqrt(sum((b*w)**2 for b, w in zip(v2, weights)))
        return dot / (norm1 * norm2 + 1e-8)
    elif method == "pearson":
        return pearson_similarity(v1, v2)
    elif method == "jaccard":
        return jaccard_similarity(v1, v2)
    elif method == "old":
        similarities = []
        for a, b, w in zip(v1, v2, weights):
            max_val = max(abs(a), abs(b), 1)
            similarities.append(w * (1 - abs(a-b)/(2*max_val)))
        return sum(similarities)/len(similarities)
    else:
        raise ValueError(f"Unknown similarity method: {method}")

# --- User-specific preferences ---
def get_user_preferences(user_id):
    # For demo: look up preferences in users_db or return None
    user = users_db.get(user_id)
    if user and hasattr(user, 'preferences'):
        return user.preferences
    return None

# --- Explanations ---
def explain_match(user1, user2, config, user_prefs=None):
    explanation = {}
    for cat in ["personality", "habit", "lifestyle", "characteristic"]:
        trait_weights = config.get("trait_weights", {})
        sim = calculate_trait_similarity_dynamic(getattr(user1, f"{cat}_score"), getattr(user2, f"{cat}_score"), method=config.get("similarity_method"), trait_weights=trait_weights)
        explanation[cat] = {"similarity": sim, "traits": {}}
        traits1 = getattr(user1, f"{cat}_score")
        traits2 = getattr(user2, f"{cat}_score")
        all_traits = set(traits1.keys()) | set(traits2.keys())
        for trait in all_traits:
            val1 = traits1.get(trait, 0)
            val2 = traits2.get(trait, 0)
            t_weight = trait_weights.get(trait, 1.0)
            explanation[cat]["traits"][trait] = {
                "user1": val1, "user2": val2, "weight": t_weight, "similarity": 1 - abs(val1-val2)/(2*max(abs(val1), abs(val2), 1))
            }
    return explanation

# --- Compatibility calculation using all improvements ---
def calculate_compatibility_dynamic(user1, user2, user1_prefs=None):
    config = matching_config
    total = 0
    total_weight = 0
    explanation = {}
    for cat in ["personality", "habit", "lifestyle", "characteristic"]:
        trait_weights = config.get("trait_weights", {})
        sim = calculate_trait_similarity_dynamic(
            getattr(user1, f"{cat}_score"),
            getattr(user2, f"{cat}_score"),
            method=config.get("similarity_method"),
            trait_weights=trait_weights,
            impute_user=user1
        )
        weight = config["category_weights"].get(cat, 1.0)
        if user1_prefs and cat in user1_prefs:
            weight *= user1_prefs[cat]
        total += sim * weight
        total_weight += weight
        explanation[cat] = sim
    penalty = cross_trait_penalty(user1, user2)
    score = max(0, (total / total_weight) - penalty)
    return score, explanation

# --- Extended EloMatcher (keeps old logic for compatibility) ---
class DynamicEloMatcher(EloMatcher):
    def calculate_compatibility_score(self, user1: UserProfile, user2: UserProfile, user1_prefs=None) -> float:
        score, _ = calculate_compatibility_dynamic(user1, user2, user1_prefs)
        return score

# Use the dynamic matcher for new matches
matcher_dynamic = DynamicEloMatcher()

# --- Adaptive learning in /rate-match (extends old endpoint) ---
from fastapi import APIRouter
router = APIRouter()

@router.post("/rate-match-dynamic")
async def rate_match_dynamic(user_id: str, other_user_id: str, rating: float):
    if user_id not in users_db or other_user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    if not 0 <= rating <= 1:
        raise HTTPException(status_code=400, detail="Rating must be between 0 and 1")
    user1 = users_db[user_id]
    user2 = users_db[other_user_id]
    matcher_dynamic.update_ratings(user1, user2, rating)
    config = matching_config
    feedback_history = config.get("feedback_history", [])
    feedback_history.append({
        "user_id": user_id,
        "other_user_id": other_user_id,
        "rating": rating,
        "timestamp": datetime.utcnow().isoformat()
    })
    config["feedback_history"] = feedback_history[-1000:]
    # --- Adaptive learning: penalize or reward ---
    min_cat = None
    min_sim = 1.0
    min_trait = None
    min_trait_sim = 1.0
    max_cat = None
    max_sim = -1.0
    max_trait = None
    max_trait_sim = -1.0
    for cat in ["personality", "habit", "lifestyle", "characteristic"]:
        trait_weights = config.get("trait_weights", {})
        sim = calculate_trait_similarity_dynamic(getattr(user1, f"{cat}_score"), getattr(user2, f"{cat}_score"), method=config.get("similarity_method"), trait_weights=trait_weights)
        if sim < min_sim:
            min_sim = sim
            min_cat = cat
        if sim > max_sim:
            max_sim = sim
            max_cat = cat
    # Find lowest and highest matching trait in those categories
    if min_cat:
        traits1 = getattr(user1, f"{min_cat}_score")
        traits2 = getattr(user2, f"{min_cat}_score")
        all_traits = set(traits1.keys()) | set(traits2.keys())
        for trait in all_traits:
            val1 = traits1.get(trait, 0)
            val2 = traits2.get(trait, 0)
            sim = 1 - abs(val1 - val2) / (2 * max(abs(val1), abs(val2), 1))
            if sim < min_trait_sim:
                min_trait_sim = sim
                min_trait = trait
    if max_cat:
        traits1 = getattr(user1, f"{max_cat}_score")
        traits2 = getattr(user2, f"{max_cat}_score")
        all_traits = set(traits1.keys()) | set(traits2.keys())
        for trait in all_traits:
            val1 = traits1.get(trait, 0)
            val2 = traits2.get(trait, 0)
            sim = 1 - abs(val1 - val2) / (2 * max(abs(val1), abs(val2), 1))
            if sim > max_trait_sim:
                max_trait_sim = sim
                max_trait = trait
    # Penalize or reward
    if rating < 0.5:
        if min_cat:
            config["category_weights"][min_cat] = max(0.05, config["category_weights"].get(min_cat, 0.1) * 0.95)
            if min_trait:
                trait_weights = config.get("trait_weights", {})
                trait_weights[min_trait] = max(0.05, trait_weights.get(min_trait, 1.0) * 0.95)
                config["trait_weights"] = trait_weights
    if rating > 0.8:
        if max_cat:
            config["category_weights"][max_cat] = min(2.0, config["category_weights"].get(max_cat, 1.0) * 1.05)
            if max_trait:
                trait_weights = config.get("trait_weights", {})
                trait_weights[max_trait] = min(2.0, trait_weights.get(max_trait, 1.0) * 1.05)
                config["trait_weights"] = trait_weights
    with open(CONFIG_PATH, 'w') as f:
        _json.dump(config, f, indent=2)
    user1.updated_at = datetime.utcnow()
    user2.updated_at = datetime.utcnow()
    return {"message": "Rating submitted successfully (dynamic, adaptive)", "updated_config": config}

# --- Explanations in match endpoint example ---
@router.post("/explain-match")
async def explain_match_endpoint(user_id: str, other_user_id: str):
    if user_id not in users_db or other_user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    user1 = users_db[user_id]
    user2 = users_db[other_user_id]
    user1_prefs = get_user_preferences(user_id)
    config = matching_config
    score, explanation = calculate_compatibility_dynamic(user1, user2, user1_prefs)
    return {"score": score, "explanation": explanation}

app.include_router(router)

# --- Documentation for extensibility ---
"""
To add a new trait or category:
1. Add the new trait/category to the config file (matching_config.json) if you want to weight it.
2. Add new questions in initialize_questions() with the new trait/category in their score dict.
3. No code changes are needed for matching logic; it will adapt automatically.
"""

# Initialize complex questionnaire
def initialize_questions():
    questions = [
        # STUDY HABITS
        Question(
            id="study_environment",
            text="What's your ideal study environment?",
            category=QuestionCategory.STUDY_HABITS,
            type=QuestionType.HABIT,
            weight=1.5,
            options=[
                {"value": "absolute_silence", "text": "Absolute silence", "score": {"noise_tolerance": -2, "focus": 2}},
                {"value": "background_music", "text": "Background music", "score": {"noise_tolerance": 1, "creativity": 1}},
                {"value": "group_study", "text": "Group study sessions", "score": {"social_preferences": 2, "collaboration": 2}},
                {"value": "cafe_ambience", "text": "Cafe ambience", "score": {"noise_tolerance": 1, "social_preferences": 1}}
            ]
        ),
        Question(
            id="study_schedule",
            text="When do you prefer to study?",
            category=QuestionCategory.STUDY_HABITS,
            type=QuestionType.HABIT,
            weight=1.2,
            options=[
                {"value": "early_morning", "text": "Early morning (6-10 AM)", "score": {"sleep_schedule": -2, "productivity": 1}},
                {"value": "daytime", "text": "Daytime (10 AM-6 PM)", "score": {"routine": 1, "social_preferences": 1}},
                {"value": "evening", "text": "Evening (6-10 PM)", "score": {"sleep_schedule": 1, "focus": 1}},
                {"value": "late_night", "text": "Late night (10 PM-2 AM)", "score": {"sleep_schedule": 2, "noise_tolerance": -1}}
            ]
        ),
        
        # SOCIAL PREFERENCES
        Question(
            id="social_energy",
            text="How do you recharge your social energy?",
            category=QuestionCategory.SOCIAL_PREFERENCES,
            type=QuestionType.PERSONALITY,
            weight=1.8,
            options=[
                {"value": "introvert", "text": "Alone time", "score": {"personal_space": 2, "social_preferences": -2}},
                {"value": "ambivert", "text": "Mix of alone time and socializing", "score": {"balance": 1, "adaptability": 1}},
                {"value": "extrovert", "text": "Socializing with others", "score": {"social_preferences": 2, "communication_style": 1}}
            ]
        ),
        Question(
            id="guest_preferences",
            text="How do you feel about having guests over?",
            category=QuestionCategory.GUEST_PREFERENCES,
            type=QuestionType.LIFESTYLE,
            weight=1.3,
            options=[
                {"value": "frequent_guests", "text": "Love having people over frequently", "score": {"social_preferences": 2, "noise_tolerance": 1}},
                {"value": "occasional_guests", "text": "Occasional guests are fine", "score": {"balance": 1, "communication_style": 1}},
                {"value": "rare_guests", "text": "Prefer rare, planned visits", "score": {"personal_space": 1, "routine": 1}},
                {"value": "no_guests", "text": "Prefer no guests", "score": {"personal_space": 2, "social_preferences": -2}}
            ]
        ),
        
        # SLEEP SCHEDULE
        Question(
            id="sleep_schedule",
            text="What's your typical sleep schedule?",
            category=QuestionCategory.SLEEP_SCHEDULE,
            type=QuestionType.LIFESTYLE,
            weight=1.6,
            options=[
                {"value": "early_bird", "text": "Early to bed, early to rise (10 PM-6 AM)", "score": {"routine": 2, "productivity": 1}},
                {"value": "normal", "text": "Normal schedule (11 PM-7 AM)", "score": {"balance": 1, "social_preferences": 1}},
                {"value": "night_owl", "text": "Late to bed, late to rise (1 AM-9 AM)", "score": {"sleep_schedule": 2, "noise_tolerance": -1}},
                {"value": "irregular", "text": "Irregular schedule", "score": {"adaptability": 1, "routine": -2}}
            ]
        ),
        
        # CLEANLINESS
        Question(
            id="cleanliness_standards",
            text="How would you describe your cleanliness standards?",
            category=QuestionCategory.CLEANLINESS,
            type=QuestionType.CHARACTERISTIC,
            weight=1.4,
            options=[
                {"value": "very_clean", "text": "Very clean and organized", "score": {"cleanliness": 2, "routine": 1}},
                {"value": "moderately_clean", "text": "Moderately clean", "score": {"cleanliness": 1, "balance": 1}},
                {"value": "relaxed", "text": "Relaxed about cleanliness", "score": {"cleanliness": -1, "adaptability": 1}},
                {"value": "messy", "text": "Messy and disorganized", "score": {"cleanliness": -2, "routine": -1}}
            ]
        ),
        
        # NOISE TOLERANCE
        Question(
            id="noise_tolerance",
            text="How sensitive are you to noise?",
            category=QuestionCategory.NOISE_TOLERANCE,
            type=QuestionType.CHARACTERISTIC,
            weight=1.5,
            options=[
                {"value": "very_sensitive", "text": "Very sensitive - need quiet", "score": {"noise_tolerance": -2, "focus": 2}},
                {"value": "moderately_sensitive", "text": "Moderately sensitive", "score": {"noise_tolerance": -1, "balance": 1}},
                {"value": "tolerant", "text": "Tolerant of moderate noise", "score": {"noise_tolerance": 1, "adaptability": 1}},
                {"value": "very_tolerant", "text": "Very tolerant - noise doesn't bother me", "score": {"noise_tolerance": 2, "social_preferences": 1}}
            ]
        ),
        
        # FINANCIAL ATTITUDE
        Question(
            id="financial_attitude",
            text="How do you approach shared expenses?",
            category=QuestionCategory.FINANCIAL_ATTITUDE,
            type=QuestionType.CHARACTERISTIC,
            weight=1.2,
            options=[
                {"value": "very_organized", "text": "Very organized and track everything", "score": {"financial_attitude": 2, "routine": 1}},
                {"value": "fairly_organized", "text": "Fairly organized", "score": {"financial_attitude": 1, "balance": 1}},
                {"value": "relaxed", "text": "Relaxed about it", "score": {"financial_attitude": -1, "adaptability": 1}},
                {"value": "very_relaxed", "text": "Very relaxed - don't track much", "score": {"financial_attitude": -2, "routine": -1}}
            ]
        ),
        
        # COMMUNICATION STYLE
        Question(
            id="communication_style",
            text="How do you prefer to communicate about issues?",
            category=QuestionCategory.COMMUNICATION_STYLE,
            type=QuestionType.PERSONALITY,
            weight=1.7,
            options=[
                {"value": "direct", "text": "Direct and immediate", "score": {"communication_style": 2, "conflict_resolution": 1}},
                {"value": "calm_discussion", "text": "Calm discussion when convenient", "score": {"communication_style": 1, "conflict_resolution": 2}},
                {"value": "written", "text": "Written communication", "score": {"communication_style": 1, "personal_space": 1}},
                {"value": "avoid_conflict", "text": "Avoid conflict when possible", "score": {"communication_style": -1, "conflict_resolution": -1}}
            ]
        ),
        
        # CONFLICT RESOLUTION
        Question(
            id="conflict_resolution",
            text="How do you handle disagreements?",
            category=QuestionCategory.CONFLICT_RESOLUTION,
            type=QuestionType.PERSONALITY,
            weight=1.6,
            options=[
                {"value": "immediate_resolution", "text": "Address immediately", "score": {"conflict_resolution": 2, "communication_style": 1}},
                {"value": "cool_down", "text": "Take time to cool down first", "score": {"conflict_resolution": 1, "personal_space": 1}},
                {"value": "compromise", "text": "Seek compromise", "score": {"conflict_resolution": 2, "adaptability": 1}},
                {"value": "avoid", "text": "Avoid confrontation", "score": {"conflict_resolution": -1, "communication_style": -1}}
            ]
        ),
        
        # PERSONAL SPACE
        Question(
            id="personal_space",
            text="How much personal space do you need?",
            category=QuestionCategory.PERSONAL_SPACE,
            type=QuestionType.CHARACTERISTIC,
            weight=1.3,
            options=[
                {"value": "lots_of_space", "text": "Need lots of personal space", "score": {"personal_space": 2, "social_preferences": -1}},
                {"value": "moderate_space", "text": "Moderate amount", "score": {"personal_space": 1, "balance": 1}},
                {"value": "minimal_space", "text": "Minimal personal space needed", "score": {"personal_space": -1, "social_preferences": 1}},
                {"value": "no_boundaries", "text": "No strict boundaries", "score": {"personal_space": -2, "social_preferences": 2}}
            ]
        ),
        
        # ADDITIONAL HABIT QUESTIONS
        Question(
            id="cooking_habits",
            text="How often do you cook at home?",
            category=QuestionCategory.LIFESTYLE,
            type=QuestionType.HABIT,
            weight=1.1,
            options=[
                {"value": "daily_cooking", "text": "Cook daily", "score": {"routine": 1, "lifestyle": 1}},
                {"value": "weekly_cooking", "text": "Cook a few times a week", "score": {"balance": 1, "lifestyle": 1}},
                {"value": "occasional_cooking", "text": "Occasionally cook", "score": {"adaptability": 1, "lifestyle": 0}},
                {"value": "rarely_cook", "text": "Rarely cook", "score": {"routine": -1, "lifestyle": -1}}
            ]
        ),
        Question(
            id="exercise_habits",
            text="How do you prefer to exercise?",
            category=QuestionCategory.LIFESTYLE,
            type=QuestionType.HABIT,
            weight=1.0,
            options=[
                {"value": "gym_workouts", "text": "Gym workouts", "score": {"routine": 1, "lifestyle": 1}},
                {"value": "outdoor_activities", "text": "Outdoor activities", "score": {"lifestyle": 1, "social_preferences": 1}},
                {"value": "home_workouts", "text": "Home workouts", "score": {"personal_space": 1, "routine": 1}},
                {"value": "no_exercise", "text": "Don't exercise regularly", "score": {"lifestyle": -1, "routine": -1}}
            ]
        )
    ]
    
    for question in questions:
        questions_db.append(question)

# Elo-style matching algorithm
class EloMatcher:
    def __init__(self, k_factor=32):
        self.k_factor = k_factor
    
    def calculate_compatibility_score(self, user1: UserProfile, user2: UserProfile) -> float:
        """Calculate compatibility score between two users using Elo-style algorithm"""
        
        # Calculate trait similarities
        personality_similarity = self._calculate_trait_similarity(
            user1.personality_score, user2.personality_score
        )
        habit_similarity = self._calculate_trait_similarity(
            user1.habit_score, user2.habit_score
        )
        lifestyle_similarity = self._calculate_trait_similarity(
            user1.lifestyle_score, user2.lifestyle_score
        )
        characteristic_similarity = self._calculate_trait_similarity(
            user1.characteristic_score, user2.characteristic_score
        )
        
        # Weighted average of similarities
        total_similarity = (
            personality_similarity * 0.3 +
            habit_similarity * 0.25 +
            lifestyle_similarity * 0.25 +
            characteristic_similarity * 0.2
        )
        
        # Convert to Elo-style rating difference
        rating_diff = (total_similarity - 0.5) * 400  # Scale to typical Elo range
        
        # Calculate expected score using Elo formula
        expected_score = 1 / (1 + 10 ** (-rating_diff / 400))
        
        return expected_score
    
    def _calculate_trait_similarity(self, traits1: Dict[str, float], traits2: Dict[str, float]) -> float:
        """Calculate similarity between two trait dictionaries"""
        if not traits1 or not traits2:
            return 0.5  # Neutral similarity if no traits
        
        # Get all unique traits
        all_traits = set(traits1.keys()) | set(traits2.keys())
        if not all_traits:
            return 0.5
        
        similarities = []
        for trait in all_traits:
            val1 = traits1.get(trait, 0)
            val2 = traits2.get(trait, 0)
            
            # Calculate similarity for this trait (0-1 scale)
            max_val = max(abs(val1), abs(val2), 1)
            similarity = 1 - abs(val1 - val2) / (2 * max_val)
            similarities.append(similarity)
        
        return sum(similarities) / len(similarities)
    
    def update_ratings(self, user1: UserProfile, user2: UserProfile, actual_score: float):
        """Update Elo ratings based on actual compatibility score"""
        expected_score = self.calculate_compatibility_score(user1, user2)
        
        # Calculate rating changes
        rating_change = self.k_factor * (actual_score - expected_score)
        
        # Update ratings
        user1.elo_rating += rating_change
        user2.elo_rating -= rating_change
        
        # Ensure ratings stay positive
        user1.elo_rating = max(100, user1.elo_rating)
        user2.elo_rating = max(100, user2.elo_rating)

# Initialize matcher
matcher = EloMatcher()

# Helper functions
def calculate_user_scores(user_profile: UserProfile) -> UserProfile:
    """Calculate personality, habit, lifestyle, and characteristic scores from responses"""
    
    # Initialize score dictionaries
    personality_scores = {}
    habit_scores = {}
    lifestyle_scores = {}
    characteristic_scores = {}
    
    for response in user_profile.responses:
        question = next((q for q in questions_db if q.id == response.question_id), None)
        if not question:
            continue
        
        # Find the selected option
        selected_option = next((opt for opt in question.options if opt["value"] == response.answer), None)
        if not selected_option:
            continue
        
        # Apply scores based on question type and weight
        weight = question.weight * response.confidence
        
        for trait, score in selected_option.get("score", {}).items():
            adjusted_score = score * weight
            
            if question.type == QuestionType.PERSONALITY:
                personality_scores[trait] = personality_scores.get(trait, 0) + adjusted_score
            elif question.type == QuestionType.HABIT:
                habit_scores[trait] = habit_scores.get(trait, 0) + adjusted_score
            elif question.type == QuestionType.LIFESTYLE:
                lifestyle_scores[trait] = lifestyle_scores.get(trait, 0) + adjusted_score
            elif question.type == QuestionType.CHARACTERISTIC:
                characteristic_scores[trait] = characteristic_scores.get(trait, 0) + adjusted_score
    
    # Normalize scores
    user_profile.personality_score = _normalize_scores(personality_scores)
    user_profile.habit_score = _normalize_scores(habit_scores)
    user_profile.lifestyle_score = _normalize_scores(lifestyle_scores)
    user_profile.characteristic_score = _normalize_scores(characteristic_scores)
    
    return user_profile

def _normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """Normalize scores to a reasonable range"""
    if not scores:
        return {}
    
    max_abs_score = max(abs(score) for score in scores.values())
    if max_abs_score == 0:
        return scores
    
    return {trait: score / max_abs_score * 2 for trait, score in scores.items()}

def find_common_traits(user1: UserProfile, user2: UserProfile) -> List[str]:
    """Find common positive traits between two users"""
    common_traits = []
    
    for trait_dict in [user1.personality_score, user1.habit_score, user1.lifestyle_score, user1.characteristic_score]:
        for trait, score in trait_dict.items():
            if score > 0.5:  # Strong positive trait
                # Check if other user has similar positive trait
                for other_dict in [user2.personality_score, user2.habit_score, user2.lifestyle_score, user2.characteristic_score]:
                    if trait in other_dict and other_dict[trait] > 0.3:
                        common_traits.append(trait)
                        break
    
    return list(set(common_traits))[:5]  # Return top 5 unique traits

def find_potential_conflicts(user1: UserProfile, user2: UserProfile) -> List[str]:
    """Find potential conflict areas between two users"""
    conflicts = []
    
    # Check for opposing traits
    for trait_dict1 in [user1.personality_score, user1.habit_score, user1.lifestyle_score, user1.characteristic_score]:
        for trait, score1 in trait_dict1.items():
            if abs(score1) > 0.7:  # Strong trait
                for trait_dict2 in [user2.personality_score, user2.habit_score, user2.lifestyle_score, user2.characteristic_score]:
                    if trait in trait_dict2:
                        score2 = trait_dict2[trait]
                        if (score1 > 0.5 and score2 < -0.5) or (score1 < -0.5 and score2 > 0.5):
                            conflicts.append(f"Opposing {trait} preferences")
                            break
    
    return list(set(conflicts))[:3]  # Return top 3 unique conflicts

# Mock profiles for demo matching
mock_profiles = [
    {
        "name": "Alex (The Early Bird)",
        "email": "alex@mock.com",
        "personality_score": {"communication_style": 1.5, "conflict_resolution": 1.2},
        "habit_score": {"routine": 2.0, "focus": 1.8},
        "lifestyle_score": {"sleep_schedule": -2.0, "social_preferences": 0.5},
        "characteristic_score": {"cleanliness": 1.8, "noise_tolerance": 1.0}
    },
    {
        "name": "Jamie (The Night Owl)",
        "email": "jamie@mock.com",
        "personality_score": {"communication_style": 0.2, "conflict_resolution": -1.0},
        "habit_score": {"routine": -1.5, "focus": 0.5},
        "lifestyle_score": {"sleep_schedule": 2.0, "social_preferences": 1.5},
        "characteristic_score": {"cleanliness": -1.0, "noise_tolerance": 2.0}
    },
    {
        "name": "Morgan (The Social Butterfly)",
        "email": "morgan@mock.com",
        "personality_score": {"communication_style": 2.0, "conflict_resolution": 1.5},
        "habit_score": {"routine": 0.5, "focus": 0.5},
        "lifestyle_score": {"sleep_schedule": 0.5, "social_preferences": 2.0},
        "characteristic_score": {"cleanliness": 0.5, "noise_tolerance": 1.5}
    },
    {
        "name": "Taylor (The Quiet Organizer)",
        "email": "taylor@mock.com",
        "personality_score": {"communication_style": 1.0, "conflict_resolution": 2.0},
        "habit_score": {"routine": 1.8, "focus": 2.0},
        "lifestyle_score": {"sleep_schedule": -1.5, "social_preferences": -1.0},
        "characteristic_score": {"cleanliness": 2.0, "noise_tolerance": -2.0}
    },
    {
        "name": "Sam (The Flexible Friend)",
        "email": "sam@mock.com",
        "personality_score": {"communication_style": 0.5, "conflict_resolution": 0.5},
        "habit_score": {"routine": 0.0, "focus": 0.0},
        "lifestyle_score": {"sleep_schedule": 0.0, "social_preferences": 0.0},
        "characteristic_score": {"cleanliness": 0.0, "noise_tolerance": 0.0}
    }
]

# API Endpoints
@app.on_event("startup")
async def startup_event():
    initialize_questions()

@app.get("/questions")
async def get_questions():
    """Get all questionnaire questions"""
    return {
        "questions": [
            {
                "id": q.id,
                "text": q.text,
                "category": q.category,
                "type": q.type,
                "weight": q.weight,
                "options": [{"value": opt["value"], "text": opt["text"]} for opt in q.options],
                "required": q.required
            }
            for q in questions_db
        ]
    }

@app.post("/submit-profile")
async def submit_profile(request: SubmitProfileRequest):
    email = request.email
    responses = request.responses
    # Validate responses
    if len(responses) < len([q for q in questions_db if q.required]):
        raise HTTPException(status_code=400, detail="Missing required questions")
    # Create user profile
    user_id = str(uuid.uuid4())
    now = datetime.utcnow()
    user_profile = UserProfile(
        user_id=user_id,
        email=email,
        responses=responses,
        created_at=now,
        updated_at=now
    )
    # Calculate scores
    user_profile = calculate_user_scores(user_profile)
    # Store user
    users_db[user_id] = user_profile
    return {
        "user_id": user_id,
        "message": "Profile submitted successfully",
        "scores": {
            "personality": user_profile.personality_score,
            "habits": user_profile.habit_score,
            "lifestyle": user_profile.lifestyle_score,
            "characteristics": user_profile.characteristic_score
        }
    }

@app.post("/find-matches")
async def find_matches(request: MatchRequest):
    """Find compatible matches for a user"""
    
    if request.user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[request.user_id]
    matches = []
    
    for other_user_id, other_user in users_db.items():
        if other_user_id == request.user_id:
            continue
        
        # Calculate compatibility
        compatibility_score = matcher.calculate_compatibility_score(user, other_user)
        
        # Calculate individual category matches
        personality_match = matcher._calculate_trait_similarity(
            user.personality_score, other_user.personality_score
        )
        habit_match = matcher._calculate_trait_similarity(
            user.habit_score, other_user.habit_score
        )
        lifestyle_match = matcher._calculate_trait_similarity(
            user.lifestyle_score, other_user.lifestyle_score
        )
        characteristic_match = matcher._calculate_trait_similarity(
            user.characteristic_score, other_user.characteristic_score
        )
        
        # Find common traits and conflicts
        common_traits = find_common_traits(user, other_user)
        potential_conflicts = find_potential_conflicts(user, other_user)
        
        match_result = MatchResult(
            user_id=other_user_id,
            email=other_user.email,
            compatibility_score=compatibility_score,
            personality_match=personality_match,
            habit_match=habit_match,
            lifestyle_match=lifestyle_match,
            characteristic_match=characteristic_match,
            common_traits=common_traits,
            potential_conflicts=potential_conflicts
        )
        
        matches.append(match_result)
    
    # Sort by compatibility score and return top matches
    matches.sort(key=lambda x: x.compatibility_score, reverse=True)
    
    return {
        "matches": matches[:request.max_matches],
        "total_matches": len(matches)
    }

@app.post("/rate-match")
async def rate_match(user_id: str, other_user_id: str, rating: float):
    """Rate a match (0-1 scale) to improve future matching"""
    
    if user_id not in users_db or other_user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not 0 <= rating <= 1:
        raise HTTPException(status_code=400, detail="Rating must be between 0 and 1")
    
    user1 = users_db[user_id]
    user2 = users_db[other_user_id]
    
    # Update Elo ratings based on actual rating
    matcher.update_ratings(user1, user2, rating)
    
    # Update timestamps
    user1.updated_at = datetime.utcnow()
    user2.updated_at = datetime.utcnow()
    
    return {"message": "Rating submitted successfully"}

@app.get("/user/{user_id}")
async def get_user_profile(user_id: str):
    """Get user profile and scores"""
    
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = users_db[user_id]
    
    return {
        "user_id": user.user_id,
        "email": user.email,
        "scores": {
            "personality": user.personality_score,
            "habits": user.habit_score,
            "lifestyle": user.lifestyle_score,
            "characteristics": user.characteristic_score
        },
        "elo_rating": user.elo_rating,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

@app.get("/stats")
async def get_stats():
    """Get API statistics"""
    return {
        "total_users": len(users_db),
        "total_questions": len(questions_db),
        "question_categories": list(set(q.category for q in questions_db)),
        "question_types": list(set(q.type for q in questions_db))
    }

@app.post("/mock-matches")
async def mock_matches(scores: dict):
    """Return the top 3 mock profiles with the highest compatibility to the submitted real profile scores."""
    def trait_similarity(traits1, traits2):
        if not traits1 or not traits2:
            return 0.5
        all_traits = set(traits1.keys()) | set(traits2.keys())
        similarities = []
        for trait in all_traits:
            val1 = traits1.get(trait, 0)
            val2 = traits2.get(trait, 0)
            max_val = max(abs(val1), abs(val2), 1)
            similarity = 1 - abs(val1 - val2) / (2 * max_val)
            similarities.append(similarity)
        return sum(similarities) / len(similarities)

    real = scores
    results = []
    for mock in mock_profiles:
        personality = trait_similarity(real.get("personality_score", {}), mock["personality_score"])
        habit = trait_similarity(real.get("habit_score", {}), mock["habit_score"])
        lifestyle = trait_similarity(real.get("lifestyle_score", {}), mock["lifestyle_score"])
        characteristic = trait_similarity(real.get("characteristic_score", {}), mock["characteristic_score"])
        total = personality * 0.3 + habit * 0.25 + lifestyle * 0.25 + characteristic * 0.2
        results.append({
            "name": mock["name"],
            "email": mock["email"],
            "compatibility": round(total * 100, 1),
            "personality": round(personality * 100, 1),
            "habit": round(habit * 100, 1),
            "lifestyle": round(lifestyle * 100, 1),
            "characteristic": round(characteristic * 100, 1)
        })
    results.sort(key=lambda x: x["compatibility"], reverse=True)
    return {"top_matches": results[:3]}

def calculate_trait_similarity(traits1, traits2, method="cosine"):
    # Use cosine similarity for vectors
    if method == "cosine":
        # Fill missing traits with 0
        all_traits = set(traits1) | set(traits2)
        v1 = [traits1.get(t, 0) for t in all_traits]
        v2 = [traits2.get(t, 0) for t in all_traits]
        dot = sum(a*b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a*a for a in v1))
        norm2 = math.sqrt(sum(b*b for b in v2))
        return dot / (norm1 * norm2 + 1e-8)
    # fallback to old method if needed

def calculate_compatibility(user1, user2, category_weights, trait_weights):
    total = 0
    total_weight = 0
    for cat in ["personality", "habit", "lifestyle", "characteristic"]:
        sim = calculate_trait_similarity(getattr(user1, f"{cat}_score"), getattr(user2, f"{cat}_score"))
        weight = category_weights.get(cat, 1.0)
        total += sim * weight
        total_weight += weight
    return total / total_weight

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 