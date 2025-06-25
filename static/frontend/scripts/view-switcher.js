function setView() {
  const isMobile = window.innerWidth <= 900;
  if (isMobile) {
    document.body.classList.add('mobile-view');
    document.body.classList.remove('desktop-view');
  } else {
    document.body.classList.add('desktop-view');
    document.body.classList.remove('mobile-view');
  }
}

// Set the view on initial load
document.addEventListener('DOMContentLoaded', setView);

// Update the view on window resize
window.addEventListener('resize', setView); 