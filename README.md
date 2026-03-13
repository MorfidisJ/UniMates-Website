# UniMates Website

A modern, responsive website for UniMates — a platform that helps university students find compatible roommates through personality-based matching.

## 📚 Documentation

- **[Technical Documentation](static/scripts/QUIZ_TECHNICAL_DOCS.md)** — Comprehensive guide to the quiz system architecture, scoring algorithm, and technical implementation
- **[Project Structure](static/PROJECT_STRUCTURE.md)** — Detailed frontend architecture and development guidelines

## 🏗️ Project Structure

```
UniMates Website/
├── 📁 static/                          # Static files (Frontend)
│   ├── 📁 pages/                       # HTML pages
│   │   ├── index.html                  # Homepage
│   │   ├── about.html                  # About us page
│   │   ├── how-it-works.html           # How it works page
│   │   ├── quiz.html                   # Roommate Style Quiz
│   │   ├── quiz-bills-lifestyle.html   # Bills & lifestyle quiz
│   │   ├── matching-survey.html        # Google Form matching survey
│   │   ├── customer-feedback.html      # Customer feedback form
│   │   └── Privacy-policy.html         # Privacy policy
│   ├── 📁 styles/                      # CSS stylesheets
│   │   ├── styles.css                  # Main stylesheet (incl. phone mockup)
│   │   ├── mobile.css                  # Mobile-specific styles
│   │   ├── about-desktop.css           # About page desktop styles
│   │   ├── how-it-works-desktop.css    # How it works desktop styles
│   │   └── quiz-desktop.css            # Quiz page desktop styles
│   ├── 📁 scripts/                     # JavaScript files
│   │   ├── shared.js                   # Shared functionality
│   │   ├── email-handler.js            # Email handling logic
│   │   ├── view-switcher.js            # View switching functionality
│   │   └── QUIZ_TECHNICAL_DOCS.md      # Technical quiz system documentation
│   └── 📁 assets/
│       └── 📁 images/                  # Image files
│           ├── logo.png                # Main logo (PNG)
│           ├── logo.svg                # Vector logo (also used as favicon)
│           ├── findroommates.jpg       # App screen: Find Roommates
│           ├── myprofile.jpg           # App screen: My Profile
│           ├── mymatches.jpg           # App screen: My Matches
│           ├── househuntingjpg.jpg     # App screen: House Hunting
│           ├── settings.jpg            # App screen: Settings
│           ├── giannopoulos.jpg        # Team member photo
│           ├── Vongelis1.jpg           # Team member photo
│           ├── gkountas.jpg            # Team member photo
│           ├── morfidis.png            # Team member photo
│           ├── piraeus.png             # Supporter logo
│           ├── c.ioanninaLogo.png      # Supporter logo
│           ├── moke.png                # Supporter logo
│           ├── pointofsynergycorrect.png # Supporter logo
│           └── hustlehours.avif        # Supporter logo
├── 📁 api/                             # Backend files
│   ├── main.py                         # FastAPI application entry point
│   └── requirements.txt               # Python dependencies
├── sw.js                               # Service Worker (cache-first strategy)
├── vercel.json                         # Vercel deployment configuration
├── CNAME                               # Custom domain configuration
└── README.md                           # This file
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
   - Navigate to [static/pages/index.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/index.html:0:0-0:0) in your browser
   - Or serve the static directory with a local server

## 📱 Pages Overview

### 🏠 Homepage ([index.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/index.html:0:0-0:0))
- **Purpose**: Main landing page introducing UniMates
- **Features**:
  - Hero section with call-to-action and floating profile cards
  - Bento-grid "Why UniMates?" advantages section
  - **App Characteristics** phone mockup with 5 real app screenshots (Find Roommates, My Profile, My Matches, House Hunting, Settings) — interactive button switching
  - Scrolling "Supported By" marquee with partner logos
  - About Us teaser section

### 👥 About Us ([about.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/about.html:0:0-0:0))
- **Purpose**: Team info, supporters, and press coverage
- **Features**:
  - Team member profile cards
  - Supported By scrolling marquee
  - **Press Highlights** carousel with equal-dimension article cards
  - Achievements blog section

### 🎯 Roommate Style Quiz ([quiz.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/quiz.html:0:0-0:0))
- **Purpose**: Interactive personality quiz for roommate matching
- **Features**:
  - 10-question personality assessment
  - Real-time progress tracking
  - Animated results with personality types
  - Email collection for waitlist
  - Social sharing functionality
- **Technical Details**: See [QUIZ_TECHNICAL_DOCS.md](static/scripts/QUIZ_TECHNICAL_DOCS.md)

### ℹ️ How It Works ([how-it-works.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/how-it-works.html:0:0-0:0))
- Step-by-step process explanation with visual flow

### 🔒 Privacy Policy ([Privacy-policy.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/Privacy-policy.html:0:0-0:0))
- GDPR-compliant privacy terms and data handling policies

### 📋 Matching Survey & Feedback
- [matching-survey.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/matching-survey.html:0:0-0:0) — Embedded Google Form for compatibility preferences
- [customer-feedback.html](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/pages/customer-feedback.html:0:0-0:0) — Embedded Google Form for user feedback

## 🎨 Design System

### Color Palette
```css
--base: #e4d6a7          /* Warm cream */
--main: #0a1045          /* Deep blue */
--accent: #df4f00        /* Orange */
--accent-light: #ff7a36  /* Light orange */
--accent-dark: #a33600   /* Dark orange */
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
- **Touch-friendly** interactions

## 🔧 Technical Features

### Frontend Technologies
- **HTML5** — Semantic markup
- **CSS3** — Custom properties, glassmorphism, grid/flexbox
- **JavaScript (ES6+)** — Interactive functionality
- **Font Awesome 6** — Icon library
- **Canvas Confetti** — Celebration animations

### Backend Technologies
- **FastAPI** — Python web framework
- **Uvicorn** — ASGI server

### Performance & Caching
- **Service Worker ([sw.js](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/sw.js:0:0-0:0))** — Cache-first strategy with stale-while-revalidate for all static assets, pages, styles, scripts, and images. API calls always bypass the cache.
- **Precaching** — All 8 HTML pages, 5 CSS files, 3 JS scripts, and 15 images cached on first visit
- **Cache busting** — Bump `CACHE_VERSION` in [sw.js](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/sw.js:0:0-0:0) on each deployment

### SEO & Accessibility
- **SVG Favicon** — [logo.svg](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/assets/images/logo.svg:0:0-0:0) set as the favicon across all pages
- **Canonical URLs**, **Open Graph**, and **Twitter Card** meta tags on every page
- **Semantic HTML5** structure
- **ARIA labels** on interactive elements

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/subscribers` | Get subscriber count |
| `POST` | `/api/subscribers` | Add new subscriber |
| `POST` | `/api/compatible-choice` | Save compatibility preferences |

## 🚀 Deployment

### Vercel
- **Serverless** Python backend via `@vercel/python`
- **Static** frontend via `@vercel/static`
- **Service Worker** served at [/sw.js](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/sw.js:0:0-0:0) with `Service-Worker-Allowed: /` and `Cache-Control: no-cache` headers
- **Custom domain** via CNAME

### Environment Variables
```bash
API_KEY_V3=your_convertkit_api_key_v3
API_KEY_V4=your_convertkit_api_key_v4
FORM_ID=your_form_id
```

## 🛠️ Development

### File Organization
- **Separation of concerns**: HTML, CSS, JS in separate files
- **Modular CSS**: Per-page stylesheets + shared [styles.css](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/styles/styles.css:0:0-0:0) + [mobile.css](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/styles/mobile.css:0:0-0:0)
- **Shared utilities**: Common functions in [shared.js](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/scripts/shared.js:0:0-0:0)

### Recent Changes
| Area | Change |
|------|--------|
| Press Highlights | Fixed equal card dimensions using fixed slide height + `height: 100%` on cards |
| App Characteristics | Wired 5 real app screenshots to each feature button in the phone mockup |
| Caching | Added [sw.js](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/sw.js:0:0-0:0) Service Worker with cache-first + stale-while-revalidate strategy |
| Favicon | Added [logo.svg](cci:7://file:///c:/Users/VG/OneDrive/Desktop/UniMates/UniMates-Website/static/assets/images/logo.svg:0:0-0:0) as SVG favicon across all 8 HTML pages |

## 📞 Support

- **Email**: contact@unimates.net
- **Instagram**: [@unimates_app](https://instagram.com/unimates_app)
- **TikTok**: [@unimatesapp](https://tiktok.com/@unimatesapp)
- **YouTube**: [UniMates Channel](https://www.youtube.com/channel/UCMKHVISj443ioGYAZYRUrTQ)
- **LinkedIn**: [UniMates](https://www.linkedin.com/company/unimatesapp)

## 📄 License

Proprietary software owned by UniMates. All rights reserved.

---

**Built with ❤️ for university students worldwide**
```
