# UniMates Quiz System - Technical Documentation

## 🎯 Overview

The UniMates Roommate Style Quiz is an interactive personality assessment that helps users discover their living preferences and matches them with compatible roommate types. The system uses a sophisticated scoring algorithm to analyze user responses and generate personalized results.

## 📊 Quiz Structure

### **Question Format**
- **Total Questions**: 10
- **Question Types**: Multiple choice with 4 options each
- **Response Format**: Each option has an icon, text description, and value
- **Navigation**: Previous/Next buttons with progress tracking

### **Question Categories**
The quiz covers 10 key living preference areas:

1. **Evening Activities** - How users spend their free time
2. **Noise Level** - Preferred home environment
3. **Household Chores** - Cleaning and organization preferences
4. **Sleep Schedule** - Daily routine patterns
5. **Cooking Habits** - Food preparation preferences
6. **Sharing Preferences** - Personal space boundaries
7. **Guest Policy** - Social hosting comfort level
8. **Conflict Resolution** - Problem-solving approach
9. **Weekend Activities** - Leisure time preferences
10. **Living Space Priorities** - What matters most in a home

## 🧮 Scoring System

### **Point Allocation Algorithm**

```javascript
// Each answer contributes points to specific personality types
const answerWeights = {
  "social": {
    "entertainment": 2,      // Gaming/watching movies
    "lively": 3,            // Music and conversation
    "communal": 3,          // Happy to share everything
    "social": 3,            // Love hosting often
    "direct": 1,            // Address immediately
    "social": 2,            // Social activities
    "communal": 2           // Social atmosphere
  },
  "studious": {
    "studious": 3,          // Studying or reading
    "quiet": 3,             // Complete silence
    "organized": 2,         // Strict cleaning schedule
    "early": 1,             // Early bird
    "morning": 2,           // Morning person
    "chef": 1,              // Love cooking daily
    "casual": 1,            // Cook simple meals
    "private": 2,           // Prefer keeping things separate
    "selective": 2,         // Only close friends
    "thoughtful": 2,        // Write it down first
    "homebody": 2,          // Relaxing at home
    "focused": 2            // Productive environment
  },
  "creative": {
    "creative": 3,          // Creative hobbies
    "moderate": 1,          // Background noise is fine
    "flexible": 1,          // Share tasks as needed
    "flexible": 1,          // Varies day to day
    "casual": 1,            // Cook simple meals
    "flexible": 1,          // Depends on the item
    "moderate": 1,          // Occasional small gatherings
    "diplomatic": 1,        // Find compromise
    "creative": 2,          // Creative projects
    "inspiring": 2          // Creative inspiration
  },
  "organized": {
    "organized": 3,         // Strict cleaning schedule
    "morning": 2,           // Morning person
    "prep": 2,              // Meal prep weekly
    "selective": 2,         // Share with clear boundaries
    "moderate": 1,          // Occasional small gatherings
    "thoughtful": 2,        // Write it down first
    "active": 1,            // Active and outdoors
    "focused": 2            // Productive environment
  }
};
```

### **Scoring Process**

1. **Answer Collection**: User selects one option per question
2. **Point Calculation**: Each answer adds points to relevant personality types
3. **Dominant Type Detection**: System identifies the personality type with highest score
4. **Result Generation**: Creates personalized result based on dominant type

### **Example Scoring**

```javascript
// User answers: ["social", "moderate", "flexible", "night", "takeout", "communal", "social", "direct", "social", "communal"]

const userAnswers = ["social", "moderate", "flexible", "night", "takeout", "communal", "social", "direct", "social", "communal"];

// Calculate scores for each personality type
const scores = {
  social: 0,
  studious: 0,
  creative: 0,
  organized: 0
};

userAnswers.forEach(answer => {
  if (answerWeights.social[answer]) scores.social += answerWeights.social[answer];
  if (answerWeights.studious[answer]) scores.studious += answerWeights.studious[answer];
  if (answerWeights.creative[answer]) scores.creative += answerWeights.creative[answer];
  if (answerWeights.organized[answer]) scores.organized += answerWeights.organized[answer];
});

// Result: social: 15, studious: 2, creative: 3, organized: 1
// Dominant type: "social" → "The Social Butterfly"
```

## 🎭 Personality Types

### **1. The Social Butterfly** 🦋
- **Score Range**: 12-20 points
- **Characteristics**:
  - High social energy
  - Excellent communication
  - Very high adaptability
- **Ideal Living Environment**: Lively, communal spaces
- **Compatible With**: Creative Spirits, Active personalities
- **Best For**: Extroverts who thrive in social environments

### **2. The Focused Scholar** 📚
- **Score Range**: 10-18 points
- **Characteristics**:
  - High focus
  - Excellent organization
  - Very high discipline
- **Ideal Living Environment**: Quiet, organized spaces
- **Compatible With**: Organized Planners, Quiet personalities
- **Best For**: Students and professionals who need concentration

### **3. The Creative Spirit** 🎨
- **Score Range**: 8-16 points
- **Characteristics**:
  - High creativity
  - Excellent expression
  - Very high innovation
- **Ideal Living Environment**: Inspiring, flexible spaces
- **Compatible With**: Social Butterflies, Inspiring personalities
- **Best For**: Artists, designers, and creative professionals

### **4. The Organized Planner** 📋
- **Score Range**: 9-17 points
- **Characteristics**:
  - High organization
  - Excellent planning
  - Very high reliability
- **Ideal Living Environment**: Structured, productive spaces
- **Compatible With**: Focused Scholars, Reliable personalities
- **Best For**: Detail-oriented individuals who value structure

## 🔧 Technical Implementation

### **Question Data Structure**

```javascript
const questions = [
  {
    text: "How do you typically spend your evenings at home?",
    options: [
      { 
        icon: "🎮", 
        text: "Gaming or watching movies", 
        value: "entertainment",
        weights: { social: 2, creative: 1 }
      },
      { 
        icon: "📚", 
        text: "Studying or reading", 
        value: "studious",
        weights: { studious: 3, organized: 1 }
      },
      { 
        icon: "🎨", 
        text: "Creative hobbies", 
        value: "creative",
        weights: { creative: 3, social: 1 }
      },
      { 
        icon: "👥", 
        text: "Socializing with friends", 
        value: "social",
        weights: { social: 3, creative: 1 }
      }
    ]
  }
  // ... 9 more questions
];
```

### **Result Calculation Function**

```javascript
function calculateResult(userAnswers) {
  // Initialize personality type scores
  const personalityScores = {
    social: 0,
    studious: 0,
    creative: 0,
    organized: 0
  };

  // Calculate scores based on user answers
  userAnswers.forEach((answer, questionIndex) => {
    const question = questions[questionIndex];
    const selectedOption = question.options.find(opt => opt.value === answer);
    
    if (selectedOption && selectedOption.weights) {
      Object.entries(selectedOption.weights).forEach(([type, points]) => {
        personalityScores[type] += points;
      });
    }
  });

  // Find dominant personality type
  let dominantType = "social"; // default
  let maxScore = 0;
  
  Object.entries(personalityScores).forEach(([type, score]) => {
    if (score > maxScore) {
      maxScore = score;
      dominantType = type;
    }
  });

  // Return personality type data
  return personalityTypes[dominantType];
}
```

### **Personality Type Definitions**

```javascript
const personalityTypes = {
  "social": {
    title: "The Social Butterfly",
    icon: "🦋",
    description: "You thrive in lively environments and love connecting with people.",
    traits: [
      { label: "Social Energy", value: "High" },
      { label: "Communication", value: "Excellent" },
      { label: "Adaptability", value: "Very High" }
    ],
    compatibleWith: ["creative", "active"],
    scoreRange: { min: 12, max: 20 }
  },
  "studious": {
    title: "The Focused Scholar",
    icon: "📚",
    description: "You value quiet study time and organization.",
    traits: [
      { label: "Focus", value: "High" },
      { label: "Organization", value: "Excellent" },
      { label: "Discipline", value: "Very High" }
    ],
    compatibleWith: ["organized", "quiet"],
    scoreRange: { min: 10, max: 18 }
  },
  "creative": {
    title: "The Creative Spirit",
    icon: "🎨",
    description: "You bring art and inspiration to your living space.",
    traits: [
      { label: "Creativity", value: "High" },
      { label: "Expression", value: "Excellent" },
      { label: "Innovation", value: "Very High" }
    ],
    compatibleWith: ["social", "inspiring"],
    scoreRange: { min: 8, max: 16 }
  },
  "organized": {
    title: "The Organized Planner",
    icon: "📋",
    description: "You love structure and keeping things in order.",
    traits: [
      { label: "Organization", value: "High" },
      { label: "Planning", value: "Excellent" },
      { label: "Reliability", value: "Very High" }
    ],
    compatibleWith: ["studious", "focused"],
    scoreRange: { min: 9, max: 17 }
  }
};
```

## 🎨 Result Display System

### **Trait Calculation**

```javascript
function getTraitProgress(value) {
  const progressMap = {
    'High': 85,
    'Very High': 95,
    'Excellent': 90,
    'Moderate': 60,
    'Good': 75,
    'Average': 50
  };
  return progressMap[value] || 70;
}

function getTraitIcon(traitLabel) {
  const icons = {
    'Social Energy': '👥',
    'Focus': '🎯',
    'Creativity': '🎨',
    'Organization': '📋',
    'Communication': '💬',
    'Expression': '🎭',
    'Innovation': '💡',
    'Planning': '📅',
    'Reliability': '✅',
    'Discipline': '⚡'
  };
  return icons[traitLabel] || '⭐';
}
```

### **Compatibility System**

```javascript
function getCompatibilityIcon(type) {
  const icons = {
    'social': '🦋',
    'creative': '🎨',
    'studious': '📚',
    'organized': '📋',
    'quiet': '🤫',
    'inspiring': '✨',
    'communal': '🏠',
    'focused': '🎯',
    'active': '🏃',
    'flexible': '🔄'
  };
  return icons[type] || '💫';
}
```

## 📊 Data Flow

### **1. User Interaction Flow**
```
User clicks answer → Option selected → Next button enabled → 
Progress bar updates → Question advances → Repeat until complete
```

### **2. Result Processing Flow**
```
Quiz completed → Answers collected → Scores calculated → 
Dominant type identified → Result generated → Display animated results
```

### **3. Data Persistence Flow**
```
Results generated → Email collected → Data sent to API → 
Results stored → Success message displayed → Full results revealed
```

## 🔄 State Management

### **Quiz State Variables**

```javascript
let currentQuestionIndex = 0;        // Current question (0-9)
let userAnswers = [];               // Array of user responses
let quizCompleted = false;          // Quiz completion status
let resultsCalculated = false;      // Results calculation status
```

### **Progress Tracking**

```javascript
function updateProgress() {
  const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
  progressBar.style.width = progress + '%';
}
```

### **Answer Validation**

```javascript
function validateAnswer() {
  return userAnswers[currentQuestionIndex] !== undefined;
}

function enableNextButton() {
  nextBtn.disabled = !validateAnswer();
  nextBtn.classList.toggle('disabled', !validateAnswer());
}
```

## 🎭 Animation System

### **Question Transitions**

```javascript
function updateQuestion() {
  // Update question number
  currentQuestionSpan.textContent = currentQuestionIndex + 1;
  
  // Update question text
  questionText.textContent = questions[currentQuestionIndex].text;
  
  // Generate options with animations
  optionsGrid.innerHTML = '';
  questions[currentQuestionIndex].options.forEach((option, index) => {
    const optionDiv = document.createElement('div');
    optionDiv.className = 'answer-option';
    optionDiv.style.animationDelay = `${index * 0.1}s`;
    // ... option content
  });
  
  // Update navigation
  prevBtn.style.display = currentQuestionIndex === 0 ? 'none' : 'block';
  nextBtn.textContent = currentQuestionIndex === questions.length - 1 ? 'See Results' : 'Next';
  
  // Update progress
  updateProgress();
}
```

### **Results Animation**

```javascript
function showResults() {
  // Hide quiz, show results
  questionCard.style.display = 'none';
  resultsSection.style.display = 'block';
  
  // Calculate and display results
  const result = calculateResult(userAnswers);
  
  // Animate results with staggered delays
  setTimeout(() => {
    // Show confetti
    window.confetti({
      particleCount: 200,
      spread: 100,
      origin: { y: 0.6 },
      colors: ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
    });
  }, 500);
}
```

## 📱 Responsive Behavior

### **Mobile Optimizations**

```css
@media (max-width: 768px) {
  .options-grid {
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }
  
  .answer-option {
    padding: 1rem;
    font-size: 0.9rem;
  }
  
  .question-text {
    font-size: 1.1rem;
    line-height: 1.5;
  }
}
```

### **Touch Interactions**

```javascript
// Touch-friendly option selection
optionDiv.addEventListener('touchstart', (e) => {
  e.preventDefault();
  selectOption(option);
});

// Prevent double-tap zoom on mobile
document.addEventListener('touchend', (e) => {
  e.preventDefault();
}, { passive: false });
```

## 🔒 Data Security

### **Input Validation**

```javascript
function validateEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function sanitizeInput(input) {
  return input.trim().replace(/[<>]/g, '');
}
```

### **API Communication**

```javascript
async function submitResults(email, results) {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/subscribers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: sanitizeInput(email),
        personality_type: results.title,
        answers: userAnswers,
        timestamp: new Date().toISOString()
      })
    });
    
    return response.ok;
  } catch (error) {
    console.error('Submission error:', error);
    return false;
  }
}
```

## 📈 Analytics & Tracking

### **Quiz Metrics**

```javascript
const quizMetrics = {
  startTime: null,
  completionTime: null,
  timeSpent: 0,
  questionsAnswered: 0,
  backButtonClicks: 0,
  resultType: null
};

function trackQuizStart() {
  quizMetrics.startTime = Date.now();
}

function trackQuizCompletion() {
  quizMetrics.completionTime = Date.now();
  quizMetrics.timeSpent = quizMetrics.completionTime - quizMetrics.startTime;
  quizMetrics.resultType = calculateResult(userAnswers).title;
}
```

## 🚀 Performance Optimizations

### **Lazy Loading**

```javascript
// Load confetti library only when needed
function loadConfetti() {
  if (!window.confetti) {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js';
    document.body.appendChild(script);
  }
}
```

### **Memory Management**

```javascript
// Clean up event listeners
function cleanupQuiz() {
  // Remove option click listeners
  document.querySelectorAll('.answer-option').forEach(option => {
    option.replaceWith(option.cloneNode(true));
  });
  
  // Clear arrays
  userAnswers = [];
  currentQuestionIndex = 0;
}
```

## 🔧 Configuration

### **Quiz Settings**

```javascript
const QUIZ_CONFIG = {
  totalQuestions: 10,
  timeLimit: null, // No time limit
  allowBackNavigation: true,
  requireAllAnswers: true,
  showProgress: true,
  enableAnimations: true,
  confettiEnabled: true,
  socialSharing: true
};
```

### **Scoring Weights**

```javascript
const SCORING_WEIGHTS = {
  primaryWeight: 3,    // Strong preference
  secondaryWeight: 2,  // Moderate preference
  tertiaryWeight: 1    // Weak preference
};
```

## 📝 Future Enhancements

### **Planned Features**
1. **More personalities / Profile combination**: Personalities with more complexity
---

**This technical documentation provides a complete understanding of the UniMates quiz system's architecture, scoring algorithm, and implementation details.** 