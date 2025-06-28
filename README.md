# UniMates Website

A modern, responsive website for UniMates - a platform that helps university students find compatible roommates through personality-based matching.

## 📚 Documentation

- **[Technical Documentation](static/scripts/QUIZ_TECHNICAL_DOCS.md)** - Comprehensive guide to the quiz system architecture, scoring algorithm, and technical implementation
- **[Project Structure](static/PROJECT_STRUCTURE.md)** - Detailed frontend architecture and development guidelines

## 🏗️ Project Structure

```
UniMates Website/
├── 📁 static/                      # Static files (Frontend)
│   ├── 📁 pages/                   # HTML pages
│   │   ├── index.html              # Homepage
│   │   ├── quiz.html               # Roommate Style Quiz
│   │   ├── how-it-works.html       # How it works page
│   │   ├── about.html              # About us page
│   │   └── Privacy-policy.html     # Privacy policy
│   ├── 📁 styles/                  # CSS stylesheets
│   │   ├── styles.css              # Main stylesheet
│   │   ├── mobile.css              # Mobile-specific styles
│   │   ├── quiz-desktop.css        # Quiz page desktop styles
│   │   ├── how-it-works-desktop.css # How it works desktop styles
│   │   └── about-desktop.css       # About page desktop styles
│   ├── 📁 scripts/                # JavaScript files
│   │   ├── QUIZ_TECHNICAL_DOCS.md  # Technical quiz system documentation
│   │   ├── shared.js               # Shared functionality
│   │   ├── email-handler.js        # Email handling logic
│   │   └── view-switcher.js        # View switching functionality
│   ├── 📁 assets/                  # Static assets
│   │   ├── 📁 images/              # Image files
│   │   │   ├── logo.png            # Main logo (PNG)
│   │   │   ├── logo.svg            # Vector logo
│   │   │   ├── 1.jpg               # Homepage image 1
│   │   │   ├── 2.jpg               # Homepage image 2
│   │   │   ├── 3.jpg               # Homepage image 3
│   │   │   ├── 4.jpg               # Homepage image 4
│   │   │   ├── gkou.jpg            # Team member photo
│   │   │   ├── than.jpg            # Team member photo
│   │   │   ├── morf.jpg            # Team member photo
│   │   │   └── vogg.jpg            # Team member photo
│   │   └── 📁 email/               # Email templates
│   │       └── unimates-email-signature.html
│   └── PROJECT_STRUCTURE.md        # Frontend architecture guide
├── 📁 api/                         # Backend files
│   ├── api.py                      # API routes and handlers
│   ├── main.py                     # FastAPI application entry point
│   └── requirements.txt            # Python dependencies
├── vercel.json                     # Vercel deployment configuration
├── logo-bg.svg                     # Project logo
├── unimates-email-signature.html   # Email signature template
├── CNAME                           # Custom domain configuration
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser
- Local development server (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MorfidisJ/UniMates-Website.git
   cd UniMates-Website
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r api/requirements.txt
   ```

3. **Start the backend server**
   ```bash
   cd api
   python main.py
   ```

4. **Open the website**
   - Navigate to `static/pages/index.html` in your browser
   - Or serve the static directory with a local server

## 📱 Pages Overview

### 🏠 Homepage (`index.html`)
- **Purpose**: Main landing page introducing UniMates
- **Features**:
  - Hero section with call-to-action
  - Feature highlights
  - Team member showcase
  - Social media links
  - Animated background elements

### 🎯 Roommate Style Quiz (`quiz.html`)
- **Purpose**: Interactive personality quiz for roommate matching
- **Features**:
  - 10-question personality assessment
  - Real-time progress tracking
  - Animated results with personality types
  - Email collection for waitlist
  - Social sharing functionality
  - Enhanced animations and styling
  - **NEW**: Improved layout with footer clearance
  - **NEW**: Subtle success messages with auto-fade
  - **NEW**: Enhanced user feedback system
- **Technical Details**: See [QUIZ_TECHNICAL_DOCS.md](static/scripts/QUIZ_TECHNICAL_DOCS.md) for complete implementation guide

### ℹ️ How It Works (`how-it-works.html`)
- **Purpose**: Explains the UniMates platform process
- **Features**:
  - Step-by-step process explanation
  - Visual flow diagrams
  - Feature highlights

### 👥 About Us (`about.html`)
- **Purpose**: Team information and company details
- **Features**:
  - Team member profiles
  - Company mission and values
  - Contact information

### 🔒 Privacy Policy (`Privacy-policy.html`)
- **Purpose**: Legal privacy information
- **Features**:
  - Comprehensive privacy terms
  - Data handling policies

## 🎨 Design System

### Color Palette
```css
--base: #e4d6a7          /* Warm cream */
--main: #0a1045          /* Deep blue */
--accent: #df4f00        /* Orange */
--accent-light: #ff7a36  /* Light orange */
--accent-dark: #a33600   /* Dark orange */
--secondary: #7b8fa1     /* Gray */
--purple: #8b5cf6        /* Purple */
--cyan: #06b6d4          /* Cyan */
```

### Typography
- **Primary**: Inter (Google Fonts)
- **Display**: Space Grotesk (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800, 900

### Responsive Design
- **Mobile-first** approach
- **Breakpoints**: 768px, 1024px, 1200px
- **Flexible grid** system
- **Touch-friendly** interactions

## 🔧 Technical Features

### Frontend Technologies
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with custom properties
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icon library
- **Canvas Confetti**: Celebration animations

### Backend Technologies
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **Requests**: HTTP client for external APIs

### Key Features
- **Progressive Web App** ready
- **SEO optimized** structure
- **Accessibility** compliant
- **Cross-browser** compatible
- **Performance** optimized
- **Layout stability** with proper footer clearance
- **Enhanced UX** with subtle feedback messages

## 🎯 Quiz System

### Personality Types
1. **The Social Butterfly** 🦋
   - High social energy
   - Excellent communication
   - Very high adaptability

2. **The Focused Scholar** 📚
   - High focus
   - Excellent organization
   - Very high discipline

3. **The Creative Spirit** 🎨
   - High creativity
   - Excellent expression
   - Very high innovation

4. **The Organized Planner** 📋
   - High organization
   - Excellent planning
   - Very high reliability

### Quiz Flow
1. **10 Questions** covering living preferences
2. **Real-time progress** tracking
3. **Answer validation** and navigation
4. **Results calculation** based on dominant traits
5. **Email collection** for waitlist
6. **Enhanced results** display with animations
7. **Social sharing** functionality
8. **NEW**: Subtle success feedback with auto-fade
9. **NEW**: Improved layout preventing footer overlap

### Technical Implementation
- **Scoring Algorithm**: Weighted point system for personality type calculation
- **State Management**: Real-time tracking of user progress and answers
- **Animation System**: Staggered animations and confetti effects
- **Data Persistence**: Email collection and API integration
- **Responsive Design**: Mobile-optimized quiz experience
- **Layout Management**: Proper spacing and footer clearance
- **User Feedback**: Subtle success messages with smooth transitions

**📖 For complete technical details, see [QUIZ_TECHNICAL_DOCS.md](static/scripts/QUIZ_TECHNICAL_DOCS.md)**

## 📧 Email System

### Features
- **Waitlist signup** functionality
- **Email validation** and processing
- **Integration** with external email services
- **Template system** for consistent messaging

### Email Templates
- **UniMates Email Signature**: Professional email signature template

## 🔌 API Endpoints

### Subscribers
- `GET /api/subscribers` - Get subscriber count
- `POST /api/subscribers` - Add new subscriber

### Quiz Results
- `POST /api/quiz-results` - Save quiz results (planned)
- `POST /api/compatible-choice` - Save compatibility preferences

## 🚀 Deployment

### Vercel Deployment
- **Serverless functions** support
- **Automatic builds** from Git
- **CDN distribution** for fast loading
- **SSL certificates** included
- **Custom domain** support

### Environment Variables
```bash
API_KEY_V3=your_convertkit_api_key_v3
API_KEY_V4=your_convertkit_api_key_v4
FORM_ID=your_form_id
```

## 🛠️ Development

### File Organization
- **Separation of concerns**: HTML, CSS, JS in separate files
- **Modular CSS**: Component-based styling
- **Shared utilities**: Common functions in shared.js
- **Page-specific styles**: Individual CSS files for complex pages

### Code Quality
- **Semantic HTML**: Proper document structure
- **CSS custom properties**: Consistent theming
- **JavaScript modules**: Organized functionality
- **Error handling**: Graceful fallbacks

### Performance Optimizations
- **Image optimization**: Compressed images
- **CSS minification**: Reduced file sizes
- **Lazy loading**: Deferred non-critical resources
- **Caching strategies**: Browser and CDN caching

### Recent Improvements
- **Layout Stability**: Fixed footer overlap issues in quiz results
- **User Experience**: Added subtle success messages with auto-fade
- **Visual Polish**: Enhanced feedback system with smooth transitions
- **Code Organization**: Improved CSS structure and JavaScript functionality

## 📱 Mobile Experience

### Responsive Features
- **Touch-friendly** buttons and interactions
- **Mobile-optimized** navigation
- **Adaptive layouts** for all screen sizes
- **Performance** optimized for mobile networks

### Mobile-Specific Styles
- **Dedicated mobile.css** for mobile optimizations
- **Touch targets** sized appropriately
- **Mobile navigation** patterns
- **Optimized typography** for small screens

## 🔒 Privacy & Security

### Data Protection
- **GDPR compliant** privacy policy
- **Secure data handling** practices
- **User consent** management
- **Data minimization** principles

### Security Features
- **HTTPS enforcement** in production
- **Input validation** and sanitization
- **CSRF protection** (planned)
- **Rate limiting** (planned)

## 🎨 Animation System

### CSS Animations
- **Smooth transitions** for all interactions
- **Staggered animations** for lists and grids
- **Hover effects** for interactive elements
- **Loading states** and feedback
- **Fade-out effects** for user notifications

### JavaScript Animations
- **Confetti effects** for celebrations
- **Progress animations** for quiz completion
- **Modal animations** for overlays
- **Scroll-triggered** animations
- **Auto-fade notifications** for better UX

## 📊 Analytics & Tracking

### Planned Features
- **User behavior** tracking
- **Quiz completion** analytics
- **Conversion tracking** for waitlist signups
- **Performance monitoring**

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Test** thoroughly
5. **Submit** a pull request

### Code Standards
- **Consistent formatting** with Prettier
- **ESLint** for JavaScript quality
- **CSS linting** for style consistency
- **Accessibility** testing

## 📞 Support

### Contact Information
- **Email**: info@unimates.net
- **Social Media**: 
  - Instagram: @unimates.info
  - TikTok: @unimatesapp
  - YouTube: UniMates Channel
  - LinkedIn: UniMates Company

### Documentation
- **[Technical Documentation](static/scripts/QUIZ_TECHNICAL_DOCS.md)** - Complete quiz system implementation guide
- **[Frontend Architecture](static/PROJECT_STRUCTURE.md)** - Frontend development guidelines
- **API Documentation**: Available at `/docs` when server is running
- **Code Comments**: Inline documentation in source files
- **README**: This comprehensive guide

## 📄 License

This project is proprietary software owned by UniMates. All rights reserved.

---

**Built with ❤️ for university students worldwide** 