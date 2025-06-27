# UniMates Complex Matching System

A sophisticated roommate matching system that uses advanced personality analysis, habit assessment, lifestyle preferences, and an Elo-style scoring algorithm to find the most compatible roommates.

## 🚀 Features

### Advanced Questionnaire
- **12 Comprehensive Questions** covering multiple dimensions:
  - Study habits and environment preferences
  - Social energy and communication style
  - Sleep schedule and lifestyle patterns
  - Cleanliness standards and personal space needs
  - Noise tolerance and guest preferences
  - Financial attitude and conflict resolution

### Multi-Dimensional Scoring
- **Personality Analysis**: Communication style, conflict resolution, social preferences
- **Habit Patterns**: Study habits, exercise routines, cooking preferences
- **Lifestyle Preferences**: Sleep schedule, guest policies, daily routines
- **Characteristics**: Cleanliness, noise tolerance, personal space needs

### Elo-Style Matching Algorithm
- **Adaptive Scoring**: Ratings adjust based on user feedback and interactions
- **Weighted Compatibility**: Different traits weighted by importance
- **Conflict Detection**: Identifies potential areas of disagreement
- **Common Trait Analysis**: Highlights shared positive characteristics

## 📁 File Structure

```
├── api/
│   ├── complex_matching.py          # Main API with Elo matching algorithm
│   └── requirements_complex.txt     # Python dependencies
├── static/
│   ├── pages/
│   │   └── complex-quiz.html        # Advanced questionnaire UI
│   ├── styles/
│   │   └── complex-quiz.css         # Modern, responsive styling
│   └── scripts/
│       └── complex-quiz.js          # Frontend logic and API integration
└── COMPLEX_MATCHING_README.md       # This file
```

## 🛠️ Setup Instructions

### 1. Install API Dependencies

```bash
cd api
pip install -r requirements_complex.txt
```

### 2. Start the API Server

```bash
cd api
python complex_matching.py
```

The API will be available at `http://localhost:8000`

### 3. Access the Complex Quiz

Open `static/pages/complex-quiz.html` in your browser or serve it through your web server.

## 🔌 API Endpoints

### Core Endpoints

#### `GET /questions`
Returns all questionnaire questions with options and scoring weights.

**Response:**
```json
{
  "questions": [
    {
      "id": "study_environment",
      "text": "What's your ideal study environment?",
      "category": "study_habits",
      "type": "habit",
      "weight": 1.5,
      "options": [
        {"value": "absolute_silence", "text": "Absolute silence"},
        {"value": "background_music", "text": "Background music"}
      ],
      "required": true
    }
  ]
}
```

#### `POST /submit-profile`
Submit user responses and get calculated personality scores.

**Request:**
```json
{
  "email": "user@example.com",
  "responses": [
    {
      "question_id": "study_environment",
      "answer": "absolute_silence",
      "confidence": 1.0
    }
  ]
}
```

**Response:**
```json
{
  "user_id": "uuid-string",
  "message": "Profile submitted successfully",
  "scores": {
    "personality": {"communication_style": 0.8, "conflict_resolution": 0.6},
    "habits": {"routine": 0.9, "focus": 0.7},
    "lifestyle": {"sleep_schedule": -0.5, "social_preferences": 0.3},
    "characteristics": {"cleanliness": 0.8, "noise_tolerance": -0.9}
  }
}
```

#### `POST /find-matches`
Find compatible roommates for a user.

**Request:**
```json
{
  "user_id": "uuid-string",
  "preferences": {},
  "max_matches": 5
}
```

**Response:**
```json
{
  "matches": [
    {
      "user_id": "other-user-uuid",
      "email": "other@example.com",
      "compatibility_score": 0.85,
      "personality_match": 0.82,
      "habit_match": 0.78,
      "lifestyle_match": 0.91,
      "characteristic_match": 0.79,
      "common_traits": ["routine", "cleanliness", "focus"],
      "potential_conflicts": ["Opposing noise_tolerance preferences"]
    }
  ],
  "total_matches": 15
}
```

#### `POST /rate-match`
Rate a match to improve future matching accuracy.

**Request:**
```json
{
  "user_id": "uuid-string",
  "other_user_id": "other-uuid",
  "rating": 0.8
}
```

### Utility Endpoints

#### `GET /user/{user_id}`
Get user profile and scores.

#### `GET /stats`
Get API statistics and metrics.

## 🎯 How the Matching Works

### 1. **Question Scoring**
Each question response affects multiple trait scores:
```python
{
  "value": "absolute_silence",
  "text": "Absolute silence",
  "score": {
    "noise_tolerance": -2,  # Strong preference for quiet
    "focus": 2             # High focus ability
  }
}
```

### 2. **Trait Normalization**
Scores are normalized to a -2 to +2 scale and categorized by type:
- **Personality**: Communication, conflict resolution, social preferences
- **Habits**: Study patterns, exercise, daily routines
- **Lifestyle**: Sleep schedule, guest policies, living patterns
- **Characteristics**: Cleanliness, noise tolerance, personal space

### 3. **Elo-Style Compatibility**
```python
# Calculate similarity between users
similarity = weighted_average(
    personality_similarity * 0.3 +
    habit_similarity * 0.25 +
    lifestyle_similarity * 0.25 +
    characteristic_similarity * 0.2
)

# Convert to Elo rating difference
rating_diff = (similarity - 0.5) * 400
expected_score = 1 / (1 + 10 ** (-rating_diff / 400))
```

### 4. **Conflict Detection**
Identifies opposing preferences:
- High noise tolerance vs. low noise tolerance
- Frequent guests vs. no guests
- Early bird vs. night owl schedules

### 5. **Common Trait Analysis**
Highlights shared positive characteristics for better compatibility.

## 🎨 UI Features

### Modern Design
- **Glassmorphism Effects**: Translucent cards with backdrop blur
- **Smooth Animations**: Transitions and hover effects
- **Responsive Layout**: Works on desktop and mobile
- **Progress Tracking**: Visual progress bar through questions

### Interactive Elements
- **Real-time Validation**: Email validation and form feedback
- **Dynamic Navigation**: Previous/Next buttons with state management
- **Loading States**: Spinner animations during API calls
- **Confetti Celebration**: Visual feedback on quiz completion

### Results Display
- **Score Visualization**: Percentage-based score cards
- **Trait Analysis**: Detailed breakdown of personality characteristics
- **Match Cards**: Comprehensive compatibility information
- **Conflict Warnings**: Potential issue identification

## 🔧 Customization

### Adding New Questions
1. Add question to `initialize_questions()` in `complex_matching.py`
2. Define scoring weights and trait impacts
3. Update frontend to handle new question types

### Modifying Scoring Weights
Adjust the `weight` parameter in question definitions:
```python
Question(
    weight=1.8,  # Higher weight = more important
    # ... other parameters
)
```

### Changing Matching Algorithm
Modify the `EloMatcher` class in `complex_matching.py`:
- Adjust `k_factor` for rating update sensitivity
- Change trait similarity calculation
- Modify category weights

## 🚀 Deployment

### Production Considerations
1. **Database**: Replace in-memory storage with PostgreSQL/MySQL
2. **Authentication**: Add user authentication and session management
3. **Rate Limiting**: Implement API rate limiting
4. **CORS**: Configure CORS for cross-origin requests
5. **Environment Variables**: Use `.env` for configuration

### Example Production Setup
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn complex_matching:app -w 4 -k uvicorn.workers.UvicornWorker

# Or with Docker
docker build -t unimates-complex-api .
docker run -p 8000:8000 unimates-complex-api
```

## 📊 Performance

### Current Implementation
- **In-Memory Storage**: Fast for development and small datasets
- **Synchronous Processing**: Simple request-response pattern
- **No Caching**: Each request processed fresh

### Scalability Options
- **Database Integration**: PostgreSQL for persistent storage
- **Redis Caching**: Cache frequently accessed data
- **Background Jobs**: Celery for match processing
- **Load Balancing**: Multiple API instances

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is part of the UniMates platform. See the main LICENSE file for details.

## 🆘 Support

For questions or issues:
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the code comments for implementation details
3. Open an issue in the repository

---

**Built with ❤️ for better roommate matching** 