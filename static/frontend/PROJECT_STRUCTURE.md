# UniMates Website - Frontend Structure

## 📁 Frontend File Organization

```
frontend/
├── 📁 pages/                          # HTML pages
│   ├── index.html                     # Homepage (landing page)
│   ├── quiz.html                      # Roommate Style Quiz
│   ├── how-it-works.html              # How it works page
│   ├── about.html                     # About us page
│   └── Privacy-policy.html            # Privacy policy
├── 📁 styles/                         # CSS stylesheets
│   ├── styles.css                     # Main stylesheet (global styles)
│   ├── mobile.css                     # Mobile-specific styles
│   ├── quiz-desktop.css               # Quiz page desktop styles
│   ├── how-it-works-desktop.css       # How it works desktop styles
│   └── about-desktop.css              # About page desktop styles
├── 📁 scripts/                        # JavaScript files
│   ├── shared.js                      # Shared functionality (navigation, etc.)
│   ├── email-handler.js               # Email handling logic
│   └── view-switcher.js               # View switching functionality
└── 📁 assets/                         # Static assets
    ├── 📁 images/                     # Image files
    │   ├── logo.png                   # Main logo (PNG format)
    │   ├── logo.svg                   # Vector logo (SVG format)
    │   ├── 1.jpg                      # Homepage image 1
    │   ├── 2.jpg                      # Homepage image 2
    │   ├── 3.jpg                      # Homepage image 3
    │   ├── 4.jpg                      # Homepage image 4
    │   ├── gkou.jpg                   # Team member photo (Thomas Gkountas)
    │   ├── than.jpg                   # Team member photo (Thanasis Giannopoulos)
    │   ├── morf.jpg                   # Team member photo (Ioannis Morfidis)
    │   └── vogg.jpg                   # Team member photo (Ioannis Voggelis)
    └── 📁 email/                      # Email templates
        └── unimates-email-signature.html
```

## 🎯 Page Overview

### **🏠 Homepage (`pages/index.html`)**
- **Purpose**: Main landing page introducing UniMates
- **Features**:
  - Hero section with call-to-action
  - Feature highlights section
  - Team member showcase
  - Social media links
  - Animated background elements
- **Dependencies**:
  - `../styles/styles.css`
  - `../styles/mobile.css`
  - `../assets/images/logo.png`
  - `../scripts/shared.js`
  - `../scripts/email-handler.js`
  - `../scripts/view-switcher.js`

### **🎯 Roommate Style Quiz (`pages/quiz.html`)**
- **Purpose**: Interactive personality quiz for roommate matching
- **Features**:
  - 10-question personality assessment
  - Real-time progress tracking
  - Animated results with personality types
  - Email collection for waitlist
  - Enhanced social sharing functionality
  - Confetti animations
- **Dependencies**:
  - `../styles/styles.css`
  - `../styles/mobile.css`
  - `../styles/quiz-desktop.css`
  - `../assets/images/logo.png`
  - `../assets/images/logo.svg`
  - `../scripts/shared.js`
  - `../scripts/view-switcher.js`

### **ℹ️ How It Works (`pages/how-it-works.html`)**
- **Purpose**: Explains the UniMates platform process
- **Features**:
  - Step-by-step process explanation
  - Visual flow diagrams
  - Feature highlights
- **Dependencies**:
  - `../styles/styles.css`
  - `../styles/mobile.css`
  - `../styles/how-it-works-desktop.css`
  - `../assets/images/logo.png`
  - `../scripts/shared.js`
  - `../scripts/view-switcher.js`

### **👥 About Us (`pages/about.html`)**
- **Purpose**: Team information and company details
- **Features**:
  - Team member profiles with photos
  - Company mission and values
  - Interactive photo gallery
  - Lightbox image viewer
- **Dependencies**:
  - `../styles/styles.css`
  - `../styles/mobile.css`
  - `../styles/about-desktop.css`
  - `../assets/images/logo.png`
  - `../assets/images/gkou.jpg`
  - `../assets/images/than.jpg`
  - `../assets/images/morf.jpg`
  - `../assets/images/vogg.jpg`
  - `../assets/images/1.jpg`
  - `../assets/images/2.jpg`
  - `../assets/images/3.jpg`
  - `../assets/images/4.jpg`
  - `../scripts/shared.js`

### **🔒 Privacy Policy (`pages/Privacy-policy.html`)**
- **Purpose**: Legal privacy information
- **Features**:
  - Comprehensive privacy terms
  - Data handling policies
  - Legal compliance information
- **Dependencies**:
  - `../styles/styles.css`
  - `../styles/mobile.css`
  - `../assets/images/logo.svg`
  - `../scripts/shared.js`
  - `../scripts/view-switcher.js`

## 🎨 Stylesheet Architecture

### **📄 Main Stylesheet (`styles/styles.css`)**
- **Purpose**: Global styles and design system
- **Contains**:
  - CSS custom properties (variables)
  - Global typography settings
  - Base component styles
  - Animation keyframes
  - Utility classes
  - Color palette definitions

### **📱 Mobile Styles (`styles/mobile.css`)**
- **Purpose**: Mobile-specific optimizations
- **Contains**:
  - Mobile navigation patterns
  - Touch-friendly interactions
  - Responsive breakpoints
  - Mobile-specific animations
  - Optimized typography for small screens

### **🖥️ Page-Specific Styles**
- **`quiz-desktop.css`**: Enhanced quiz styling with animations and results display
- **`how-it-works-desktop.css`**: Desktop-specific styling for process explanation
- **`about-desktop.css`**: Team page styling with gallery and member cards

## 🔧 JavaScript Architecture

### **🤝 Shared Script (`scripts/shared.js`)**
- **Purpose**: Common functionality used across all pages
- **Features**:
  - Navigation menu handling
  - Mobile menu toggle
  - Smooth scrolling
  - Common animations
  - DOM utility functions

### **📧 Email Handler (`scripts/email-handler.js`)**
- **Purpose**: Email processing and form handling
- **Features**:
  - Email validation
  - Form submission logic
  - API communication
  - Error handling

### **🔄 View Switcher (`scripts/view-switcher.js`)**
- **Purpose**: Responsive view management
- **Features**:
  - View switching logic
  - Responsive behavior
  - Layout adjustments

## 🖼️ Asset Management

### **📸 Images (`assets/images/`)**
- **Logos**: `logo.png`, `logo.svg` - Brand identity
- **Team Photos**: Individual member photos for about page
- **Gallery Images**: Team activity photos (1.jpg, 2.jpg, 3.jpg, 4.jpg)

### **📧 Email Templates (`assets/email/`)**
- **UniMates Email Signature**: Professional email signature template

## 🔗 Path Reference System

### **Relative Paths**
All internal resources use relative paths with `../` to navigate up from pages directory:
```
pages/index.html → ../styles/styles.css
pages/quiz.html → ../scripts/shared.js
pages/about.html → ../assets/images/logo.png
```

### **External Resources**
External CDN resources use absolute URLs:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter...">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/...">
```

## 🎨 Design System

### **Color Palette**
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

### **Typography**
- **Primary**: Inter (Google Fonts)
- **Display**: Space Grotesk (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700, 800, 900

### **Responsive Breakpoints**
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🚀 Development Workflow

### **File Organization Principles**
1. **Separation of Concerns**: HTML, CSS, and JS in separate directories
2. **Modular Structure**: Page-specific styles and scripts
3. **Asset Centralization**: All images and templates in dedicated folders
4. **Scalable Architecture**: Easy to add new pages and features

### **Naming Conventions**
- **Files**: kebab-case (e.g., `how-it-works.html`)
- **Classes**: kebab-case (e.g., `nav-container`)
- **IDs**: camelCase (e.g., `quizContainer`)
- **Variables**: camelCase (e.g., `userAnswers`)

### **Maintenance Guidelines**
- **CSS**: Global styles in `styles.css`, page-specific in dedicated files
- **JavaScript**: Shared utilities in `shared.js`, page-specific in inline scripts
- **Images**: All images centralized in `assets/images/`
- **Templates**: Email templates in `assets/email/`

## 📱 Responsive Design

### **Mobile-First Approach**
- Base styles target mobile devices
- Progressive enhancement for larger screens
- Touch-friendly interactions
- Optimized performance for mobile networks

### **Cross-Browser Compatibility**
- Modern CSS features with fallbacks
- JavaScript feature detection
- Progressive enhancement
- Accessibility compliance

## 🎯 Performance Optimizations

### **Image Optimization**
- Compressed images for web
- Appropriate formats (PNG for logos, JPG for photos)
- Responsive images where needed

### **CSS Optimization**
- Efficient selectors
- Minimal specificity conflicts
- Organized cascade structure

### **JavaScript Optimization**
- Modular code structure
- Event delegation where appropriate
- Efficient DOM manipulation

## 🔒 Security Considerations

### **Frontend Security**
- Input validation
- XSS prevention
- Secure external resource loading
- HTTPS enforcement in production

## 📝 Notes

- All file paths use relative references for portability
- External resources (CDNs) remain unchanged
- The structure supports both development and production environments
- Easy to deploy to static hosting platforms
- Scalable for future feature additions 