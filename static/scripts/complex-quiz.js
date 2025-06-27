// Complex Quiz Application
class ComplexQuiz {
    constructor() {
        this.questions = [];
        this.currentQuestionIndex = 0;
        this.userResponses = [];
        this.userProfile = null;
        this.matches = [];
        
        // API Configuration
        this.apiBaseUrl = 'http://localhost:8000'; // Update with your API URL
        
        // DOM Elements
        this.elements = {
            welcomeScreen: document.getElementById('welcomeScreen'),
            questionScreen: document.getElementById('questionScreen'),
            resultsScreen: document.getElementById('resultsScreen'),
            loadingScreen: document.getElementById('loadingScreen'),
            startBtn: document.getElementById('startBtn'),
            prevBtn: document.getElementById('prevBtn'),
            nextBtn: document.getElementById('nextBtn'),
            questionText: document.getElementById('questionText'),
            categoryText: document.getElementById('categoryText'),
            questionNumber: document.getElementById('questionNumber'),
            optionsContainer: document.getElementById('optionsContainer'),
            progressFill: document.getElementById('progressFill'),
            progressText: document.getElementById('progressText'),
            emailInput: document.getElementById('emailInput'),
            findMatchesBtn: document.getElementById('findMatchesBtn'),
            matchesResults: document.getElementById('matchesResults'),
            matchesGrid: document.getElementById('matchesGrid'),
            scoreGrid: document.getElementById('scoreGrid'),
            personalityTraits: document.getElementById('personalityTraits'),
            habitTraits: document.getElementById('habitTraits'),
            lifestyleTraits: document.getElementById('lifestyleTraits'),
            characteristicTraits: document.getElementById('characteristicTraits')
        };
        
        this.profileModal = document.getElementById('profileModal');
        this.profileEmailInput = document.getElementById('profileEmailInput');
        this.profileEmailError = document.getElementById('profileEmailError');
        this.profileSubmitBtn = document.getElementById('profileSubmitBtn');
        this.profileNameInput = document.getElementById('profileNameInput');
        this.profileAgeInput = document.getElementById('profileAgeInput');
        this.userEmail = null;
        this.userName = null;
        this.userAge = null;
        
        this.initialize();
    }
    
    async initialize() {
        try {
            await this.loadQuestions();
            this.bindEvents();
            this.showWelcomeScreen();
        } catch (error) {
            this.showError('Failed to initialize quiz: ' + error.message);
        }
    }
    
    async loadQuestions() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/questions`);
            if (!response.ok) {
                throw new Error('Failed to fetch questions');
            }
            const data = await response.json();
            this.questions = data.questions;
        } catch (error) {
            console.error('Error loading questions:', error);
            this.showError('Could not connect to the server. Please make sure the API is running and try again.');
            throw error;
        }
    }
    
    bindEvents() {
        // Start button
        this.elements.startBtn.addEventListener('click', () => {
            this.startQuiz();
        });
        
        // Navigation buttons
        this.elements.prevBtn.addEventListener('click', () => {
            this.previousQuestion();
        });
        
        this.elements.nextBtn.addEventListener('click', () => {
            this.nextQuestion();
        });
        
        // Find matches button
        this.elements.findMatchesBtn.addEventListener('click', () => {
            this.findMatches();
        });
        
        // Email input validation
        this.elements.emailInput.addEventListener('input', () => {
            this.validateEmail();
        });
    }
    
    showWelcomeScreen() {
        this.elements.welcomeScreen.style.display = 'block';
        this.elements.questionScreen.style.display = 'none';
        this.elements.resultsScreen.style.display = 'none';
        this.elements.loadingScreen.style.display = 'none';
    }
    
    startQuiz() {
        this.currentQuestionIndex = 0;
        this.userResponses = [];
        this.showQuestionScreen();
        this.updateQuestion();
    }
    
    showQuestionScreen() {
        this.elements.welcomeScreen.style.display = 'none';
        this.elements.questionScreen.style.display = 'block';
        this.elements.resultsScreen.style.display = 'none';
        this.elements.loadingScreen.style.display = 'none';
    }
    
    updateQuestion() {
        if (this.currentQuestionIndex >= this.questions.length) {
            this.showResults();
            return;
        }
        
        const question = this.questions[this.currentQuestionIndex];
        
        // Update question text and category
        this.elements.questionText.textContent = question.text;
        this.elements.categoryText.textContent = this.formatCategory(question.category);
        this.elements.questionNumber.textContent = this.currentQuestionIndex + 1;
        
        // Update progress
        const progress = ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
        this.elements.progressFill.style.width = `${progress}%`;
        this.elements.progressText.textContent = `Question ${this.currentQuestionIndex + 1} of ${this.questions.length}`;
        
        // Render options
        this.renderOptions(question);
        
        // Update navigation buttons
        this.updateNavigationButtons();
    }
    
    renderOptions(question) {
        this.elements.optionsContainer.innerHTML = '';
        
        question.options.forEach((option, index) => {
            const optionElement = document.createElement('div');
            optionElement.className = 'option';
            optionElement.textContent = option.text;
            
            // Check if this option is already selected
            const currentResponse = this.userResponses[this.currentQuestionIndex];
            if (currentResponse && currentResponse.answer === option.value) {
                optionElement.classList.add('selected');
            }
            
            optionElement.addEventListener('click', () => {
                this.selectOption(option.value, optionElement);
            });
            
            this.elements.optionsContainer.appendChild(optionElement);
        });
    }
    
    selectOption(optionValue, optionElement) {
        // Remove selection from all options
        this.elements.optionsContainer.querySelectorAll('.option').forEach(opt => {
            opt.classList.remove('selected');
        });
        
        // Add selection to clicked option
        optionElement.classList.add('selected');
        
        // Store response
        this.userResponses[this.currentQuestionIndex] = {
            question_id: this.questions[this.currentQuestionIndex].id,
            answer: optionValue,
            confidence: 1.0
        };
        
        // Enable next button
        this.elements.nextBtn.disabled = false;
    }
    
    updateNavigationButtons() {
        this.elements.prevBtn.disabled = this.currentQuestionIndex === 0;
        this.elements.nextBtn.disabled = !this.userResponses[this.currentQuestionIndex];
    }
    
    previousQuestion() {
        if (this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            this.updateQuestion();
        }
    }
    
    nextQuestion() {
        if (this.currentQuestionIndex < this.questions.length - 1) {
            this.currentQuestionIndex++;
            this.updateQuestion();
        } else {
            // Prompt for profile before analyzing
            this.showProfileModal();
        }
    }
    
    showProfileModal() {
        this.profileModal.style.display = 'flex';
        this.profileNameInput.value = '';
        this.profileAgeInput.value = '';
        this.profileEmailInput.value = '';
        this.profileEmailError.style.display = 'none';
        this.profileSubmitBtn.disabled = false;
        this.profileSubmitBtn.onclick = async () => {
            const name = this.profileNameInput.value.trim();
            const age = parseInt(this.profileAgeInput.value, 10);
            const email = this.profileEmailInput.value.trim();
            if (!name) {
                this.profileEmailError.textContent = 'Please enter your name.';
                this.profileEmailError.style.display = 'block';
                return;
            }
            if (!age || age < 16 || age > 100) {
                this.profileEmailError.textContent = 'Please enter a valid age (16-100).';
                this.profileEmailError.style.display = 'block';
                return;
            }
            if (!this.isValidEmail(email)) {
                this.profileEmailError.textContent = 'Please enter a valid email address.';
                this.profileEmailError.style.display = 'block';
                return;
            }
            this.profileEmailError.style.display = 'none';
            this.profileSubmitBtn.disabled = true;
            this.userName = name;
            this.userAge = age;
            this.userEmail = email;
            this.profileModal.style.display = 'none';
            await this.showResults();
        };
    }
    
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    async showResults() {
        this.showLoadingScreen();
        try {
            await this.submitProfile();
            this.showResultsScreen();
            this.renderResults();
            await this.fetchAndShowMockMatches();
        } catch (error) {
            this.showError('Failed to process your responses. Please try again.');
        }
    }
    
    showLoadingScreen() {
        this.elements.welcomeScreen.style.display = 'none';
        this.elements.questionScreen.style.display = 'none';
        this.elements.resultsScreen.style.display = 'none';
        this.elements.loadingScreen.style.display = 'block';
    }
    
    showResultsScreen() {
        this.elements.welcomeScreen.style.display = 'none';
        this.elements.questionScreen.style.display = 'none';
        this.elements.resultsScreen.style.display = 'block';
        this.elements.loadingScreen.style.display = 'none';
    }
    
    async submitProfile() {
        console.log('Submitting profile payload:', {
            email: this.userEmail,
            responses: this.userResponses
        });
        
        // The FastAPI endpoint only expects email and responses
        const payload = {
            email: this.userEmail,
            responses: this.userResponses
        };
        
        console.log('Submitting profile payload:', payload);
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/submit-profile`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Server error:', errorData);
                throw new Error(errorData.detail || `Server error: ${response.status}`);
            }
            
            const data = await response.json();
            this.userProfile = data;
            
            // Show confetti for completion
            this.showConfetti();
            
        } catch (error) {
            console.error('Error submitting profile:', error);
            throw error;
        }
    }
    renderResults() {
        if (!this.userProfile) return;
        
        // Render score grid
        this.renderScoreGrid();
        
        // Render trait analysis
        this.renderTraitAnalysis();
    }
    
    renderScoreGrid() {
        const scores = this.userProfile.scores;
        this.elements.scoreGrid.innerHTML = '';
        
        const scoreCategories = [
            { key: 'personality', label: 'Personality', icon: 'fas fa-brain' },
            { key: 'habits', label: 'Habits', icon: 'fas fa-clock' },
            { key: 'lifestyle', label: 'Lifestyle', icon: 'fas fa-home' },
            { key: 'characteristics', label: 'Characteristics', icon: 'fas fa-user' }
        ];
        
        scoreCategories.forEach(category => {
            const scoreData = scores[category.key];
            const averageScore = Math.max(0, Math.min(1, this.calculateAverageScore(scoreData)));
            const percent = Math.round(averageScore * 100);
            
            const scoreElement = document.createElement('div');
            scoreElement.className = 'score-item';
            scoreElement.innerHTML = `
                <div class="score-label">${category.label}</div>
                <div class="score-value">${percent}%</div>
                <div class="score-bar"><div class="score-bar-fill" style="width:${percent}%;"></div></div>
            `;
            
            this.elements.scoreGrid.appendChild(scoreElement);
        });
    }
    
    renderTraitAnalysis() {
        const scores = this.userProfile.scores;
        
        // Render personality traits
        this.renderTraitsSection(this.elements.personalityTraits, scores.personality, 'Personality');
        
        // Render habit traits
        this.renderTraitsSection(this.elements.habitTraits, scores.habits, 'Habits');
        
        // Render lifestyle traits
        this.renderTraitsSection(this.elements.lifestyleTraits, scores.lifestyle, 'Lifestyle');
        
        // Render characteristic traits
        this.renderTraitsSection(this.elements.characteristicTraits, scores.characteristics, 'Characteristics');
    }
    
    renderTraitsSection(container, traits, category) {
        container.innerHTML = '';
        
        if (!traits || Object.keys(traits).length === 0) {
            container.innerHTML = '<p style="color: var(--secondary-dark); font-style: italic;">No traits available</p>';
            return;
        }
        
        // Sort traits by absolute value (strongest first)
        const sortedTraits = Object.entries(traits)
            .sort(([,a], [,b]) => Math.abs(b) - Math.abs(a))
            .slice(0, 5); // Show top 5 traits
        
        sortedTraits.forEach(([trait, value]) => {
            // Clamp value to [-1, 1] for bar
            const clamped = Math.max(-1, Math.min(1, value));
            const percent = Math.round(Math.abs(clamped) * 100);
            const traitElement = document.createElement('div');
            traitElement.className = 'trait-item';
            const traitName = this.formatTraitName(trait);
            const traitValue = clamped > 0 ? `+${percent}%` : clamped < 0 ? `-${percent}%` : '0%';
            traitElement.innerHTML = `
                <span class="trait-name">${traitName}</span>
                <div class="trait-bar"><div class="trait-bar-fill" style="width:${percent}%; background: linear-gradient(90deg, var(--accent), var(--purple), var(--cyan));"></div></div>
                <span class="trait-value">${traitValue}</span>
            `;
            container.appendChild(traitElement);
        });
    }
    
    calculateAverageScore(scores) {
        if (!scores || Object.keys(scores).length === 0) return 0;
        
        const values = Object.values(scores);
        const sum = values.reduce((acc, val) => acc + Math.abs(val), 0);
        return sum / values.length;
    }
    
    formatCategory(category) {
        return category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    formatTraitName(trait) {
        return trait.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    validateEmail() {
        const email = this.elements.emailInput.value.trim();
        const isValid = email && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
        
        this.elements.findMatchesBtn.disabled = !isValid;
        return isValid;
    }
    
    async findMatches() {
        if (!this.validateEmail()) {
            this.showError('Please enter a valid email address.');
            return;
        }
        
        if (!this.userProfile) {
            this.showError('Profile not found. Please complete the quiz first.');
            return;
        }
        
        this.elements.findMatchesBtn.disabled = true;
        this.elements.findMatchesBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Finding matches...</span>';
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/find-matches`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: this.userProfile.user_id,
                    max_matches: 5
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to find matches');
            }
            
            const data = await response.json();
            this.matches = data.matches;
            
            this.renderMatches();
            this.elements.matchesResults.style.display = 'block';
            
        } catch (error) {
            console.error('Error finding matches:', error);
            this.showError('Failed to find matches. Please try again.');
        } finally {
            this.elements.findMatchesBtn.disabled = false;
            this.elements.findMatchesBtn.innerHTML = '<i class="fas fa-search"></i><span>Find Matches</span>';
        }
    }
    
    renderMatches() {
        this.elements.matchesGrid.innerHTML = '';
        
        if (this.matches.length === 0) {
            this.elements.matchesGrid.innerHTML = `
                <div style="text-align: center; grid-column: 1 / -1; padding: 2rem;">
                    <p style="color: var(--text-secondary);">No matches found yet. Check back later!</p>
                </div>
            `;
            return;
        }
        
        this.matches.forEach(match => {
            const matchElement = document.createElement('div');
            matchElement.className = 'match-card';
            
            const compatibilityPercent = (match.compatibility_score * 100).toFixed(0);
            
            matchElement.innerHTML = `
                <div class="match-header">
                    <span class="match-email">${this.maskEmail(match.email)}</span>
                    <span class="compatibility-score">${compatibilityPercent}% Match</span>
                </div>
                
                <div class="match-details">
                    <div class="match-detail">
                        <div class="match-detail-label">Personality</div>
                        <div class="match-detail-value">${(match.personality_match * 100).toFixed(0)}%</div>
                    </div>
                    <div class="match-detail">
                        <div class="match-detail-label">Habits</div>
                        <div class="match-detail-value">${(match.habit_match * 100).toFixed(0)}%</div>
                    </div>
                    <div class="match-detail">
                        <div class="match-detail-label">Lifestyle</div>
                        <div class="match-detail-value">${(match.lifestyle_match * 100).toFixed(0)}%</div>
                    </div>
                    <div class="match-detail">
                        <div class="match-detail-label">Characteristics</div>
                        <div class="match-detail-value">${(match.characteristic_match * 100).toFixed(0)}%</div>
                    </div>
                </div>
                
                ${match.common_traits.length > 0 ? `
                    <div class="match-traits">
                        <h4>Common Traits</h4>
                        <div class="traits-list">
                            ${match.common_traits.map(trait => `<span class="trait-tag">${this.formatTraitName(trait)}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
                
                ${match.potential_conflicts.length > 0 ? `
                    <div class="conflicts-list">
                        <h4>Potential Conflicts</h4>
                        <div class="traits-list">
                            ${match.potential_conflicts.map(conflict => `<span class="conflict-tag">${conflict}</span>`).join('')}
                        </div>
                    </div>
                ` : ''}
            `;
            
            this.elements.matchesGrid.appendChild(matchElement);
        });
    }
    
    maskEmail(email) {
        const [localPart, domain] = email.split('@');
        const maskedLocal = localPart.charAt(0) + '*'.repeat(localPart.length - 2) + localPart.charAt(localPart.length - 1);
        return `${maskedLocal}@${domain}`;
    }
    
    showConfetti() {
        if (typeof window.confetti === 'function') {
            window.confetti({
                particleCount: 200,
                spread: 100,
                origin: { y: 0.6 },
                colors: ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
            });
        }
    }
    
    showError(message) {
        const toast = document.getElementById('errorToast');
        if (!toast) return;
        toast.textContent = message;
        toast.style.display = 'block';
        toast.style.opacity = '0.98';
        toast.style.pointerEvents = 'auto';
        // Hide after 4 seconds
        clearTimeout(this._errorToastTimeout);
        this._errorToastTimeout = setTimeout(() => {
            toast.style.display = 'none';
        }, 4000);
    }

    async fetchAndShowMockMatches() {
        const scores = this.userProfile && this.userProfile.scores;
        if (!scores) return;
        try {
            const response = await fetch(`${this.apiBaseUrl}/mock-matches`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    personality_score: scores.personality,
                    habit_score: scores.habits,
                    lifestyle_score: scores.lifestyle,
                    characteristic_score: scores.characteristics
                })
            });
            if (!response.ok) throw new Error('Failed to fetch mock matches');
            const data = await response.json();
            this.renderMockMatches(data.top_matches);
        } catch (error) {
            document.getElementById('mockMatchesSection').style.display = 'block';
            document.getElementById('mockMatchesGrid').innerHTML = '<div style="color:#e53e3e;">Could not load mock matches.</div>';
        }
    }

    renderMockMatches(matches) {
        const section = document.getElementById('mockMatchesSection');
        const grid = document.getElementById('mockMatchesGrid');
        if (!matches || matches.length === 0) {
            section.style.display = 'block';
            grid.innerHTML = '<div style="color:#6b7280;">No mock matches found.</div>';
            return;
        }
        section.style.display = 'block';
        grid.innerHTML = '';
        matches.forEach(match => {
            const card = document.createElement('div');
            card.className = 'match-card';
            card.innerHTML = `
                <div class="match-header">
                    <span class="match-email">${match.name}</span>
                    <span class="compatibility-score">${match.compatibility}% Match</span>
                </div>
                <div class="match-details">
                    <div class="match-detail">
                        <div class="match-detail-label">Personality</div>
                        <div class="match-detail-value">${match.personality}%</div>
                    </div>
                    <div class="match-detail">
                        <div class="match-detail-label">Habits</div>
                        <div class="match-detail-value">${match.habit}%</div>
                    </div>
                    <div class="match-detail">
                        <div class="match-detail-label">Lifestyle</div>
                        <div class="match-detail-value">${match.lifestyle}%</div>
                    </div>
                    <div class="match-detail">
                        <div class="match-detail-label">Characteristics</div>
                        <div class="match-detail-value">${match.characteristic}%</div>
                    </div>
                </div>
                <div style="color:#6366f1; font-size:0.95rem; margin-top:0.5rem;">${match.email}</div>
            `;
            grid.appendChild(card);
        });
    }
}

// Initialize the quiz when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ComplexQuiz();
}); 