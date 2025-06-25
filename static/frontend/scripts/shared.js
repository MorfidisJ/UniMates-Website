// Shared JavaScript for UniMates Website
// Contains common functionality used across all pages

// ============================================================================
// FOOTER CUBE ANIMATION
// ============================================================================
(function() {
  const cube = document.querySelector('.footer-cube-container .cube');
  if (!cube) return;
  
  let angleY = 30;
  let angleX = -20;
  let animationFrame;
  let running = true;

  function animate() {
    if (running) {
      angleY += 0.6; // speed of rotation
      if (angleY > 360) angleY -= 360;
      cube.style.transform = `rotateX(${angleX}deg) rotateY(${angleY}deg)`;
    }
    animationFrame = requestAnimationFrame(animate);
  }

  cube.addEventListener('mouseenter', () => { running = false; });
  cube.addEventListener('mouseleave', () => { running = true; });
  cube.addEventListener('focus', () => { running = false; });
  cube.addEventListener('blur', () => { running = true; });

  animate();
})();

// ============================================================================
// MOBILE MENU FUNCTIONALITY
// ============================================================================
function toggleMenu(button) {
  const navLinks = document.querySelector('.nav-links');
  const overlay = document.querySelector('.mobile-overlay');
  const body = document.body;
  const quizButton = document.querySelector('.quiz-header-ad');
  
  navLinks.classList.toggle('show');
  overlay.classList.toggle('show');
  button.classList.toggle('active');
  
  if (quizButton) {
    quizButton.classList.toggle('hidden');
  }
  
  if (navLinks.classList.contains('show')) {
    body.style.overflow = 'hidden';
  } else {
    body.style.overflow = '';
  }
}

function closeMenu() {
  const navLinks = document.querySelector('.nav-links');
  const overlay = document.querySelector('.mobile-overlay');
  const hamburger = document.querySelector('.hamburger');
  const body = document.body;
  const quizButton = document.querySelector('.quiz-header-ad');
  
  navLinks.classList.remove('show');
  overlay.classList.remove('show');
  hamburger.classList.remove('active');
  
  if (quizButton) {
    quizButton.classList.remove('hidden');
  }
  body.style.overflow = '';
}

// ============================================================================
// GENERAL EVENT LISTENERS
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
  // Handle window resize
  window.addEventListener('resize', () => {
    // Close mobile menu on desktop
    if (window.innerWidth > 768) {
      closeMenu();
    }
    
    // Update confetti canvas size if it exists
    const canvas = document.getElementById('confetti-canvas');
    if (canvas) {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
  });

  // Close menu when clicking on nav links
  document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });

  // Add touch interactions for cards (if they exist)
  document.querySelectorAll('.profile-card, .personality-card').forEach(card => {
    card.addEventListener('touchstart', function() {
      this.style.transform = 'translateY(-2px) scale(0.98)';
    });
    card.addEventListener('touchend', function() {
      this.style.transform = '';
    });
  });
});

// ============================================================================
// CONFETTI FUNCTION (for pages that need it)
// ============================================================================
function launchConfetti() {
  const canvas = document.getElementById('confetti-canvas');
  if (!canvas) return;
  
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  let confetti = [];

  for (let i = 0; i < 120; i++) {
    confetti.push({
      x: Math.random() * canvas.width,
      y: Math.random() * -canvas.height,
      r: Math.random() * 8 + 4,
      d: Math.random() * 80 + 40,
      color: `hsl(${Math.random()*360},90%,60%)`,
      tilt: Math.random() * 10 - 10,
      tiltAngle: 0,
      tiltAngleIncremental: (Math.random() * 0.07) + 0.05
    });
  }

  let angle = 0;
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    angle += 0.01;
    for (let i = 0; i < confetti.length; i++) {
      let c = confetti[i];
      c.y += (Math.cos(angle + c.d) + 3 + c.r / 2) * 0.7;
      c.x += Math.sin(angle);
      c.tiltAngle += c.tiltAngleIncremental;
      c.tilt = Math.sin(c.tiltAngle) * 15;
      ctx.beginPath();
      ctx.lineWidth = c.r;
      ctx.strokeStyle = c.color;
      ctx.moveTo(c.x + c.tilt + c.r / 3, c.y);
      ctx.lineTo(c.x + c.tilt, c.y + c.tilt + c.r);
      ctx.stroke();
    }
    confetti = confetti.filter(c => c.y < canvas.height + 20);
    if (confetti.length > 0) requestAnimationFrame(draw);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  draw();
} 