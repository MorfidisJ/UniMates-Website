
class EmailHandler {
  constructor(apiBaseUrl = 'http://localhost:8000') {
    this.apiBaseUrl = apiBaseUrl;
  }

  /**
   * Submit email to the waitlist
   * @param {string} email - User's email address
   * @param {string} firstName - User's first name (optional)
   * @returns {Promise<Object>} Response from the API
   */
  async submitEmail(email, firstName = null) {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/subscribers`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email,
          first_name: firstName
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error submitting email:', error);
      throw error;
    }
  }

  /**
   * Get subscriber count
   * @returns {Promise<number>} Number of subscribers
   */
  async getSubscriberCount() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/subscribers`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data.subscriber_count;
    } catch (error) {
      console.error('Error getting subscriber count:', error);
      throw error;
    }
  }
}

// Initialize the email handler
const emailHandler = new EmailHandler();

// Enhanced form handling with API integration
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('waitlistForm');
  const emailInput = document.getElementById('email');
  const consentCheckbox = document.getElementById('consent');
  const submitButton = form.querySelector('button[type="submit"]');
  const successMessage = document.getElementById('successMessage');

  // Helper function to validate email
  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }

  // Update button state based on form validity
  function updateSubmitButton() {
    const isEmailValid = isValidEmail(emailInput.value);
    const isConsentChecked = consentCheckbox.checked;
    submitButton.disabled = !(isEmailValid && isConsentChecked);
  }

  // Show loading state
  function setLoadingState(loading) {
    if (loading) {
      submitButton.disabled = true;
      submitButton.innerHTML = '<span>Joining...</span>';
      submitButton.classList.add('loading');
    } else {
      submitButton.innerHTML = 'Join Waitlist';
      submitButton.classList.remove('loading');
      updateSubmitButton(); // Reset to proper state
    }
  }

  // Show error message
  function showError(message) {
    // Remove any existing error messages
    const existingError = form.querySelector('.error-message');
    if (existingError) {
      existingError.remove();
    }

    // Create and show error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.style.cssText = `
      color: #e74c3c;
      background: #fdf2f2;
      border: 1px solid #f5c6cb;
      padding: 12px;
      border-radius: 8px;
      margin-top: 10px;
      font-size: 14px;
      text-align: center;
    `;
    errorDiv.textContent = message;
    form.appendChild(errorDiv);

    // Remove error after 5 seconds
    setTimeout(() => {
      if (errorDiv.parentNode) {
        errorDiv.remove();
      }
    }, 5000);
  }

  // Extract first name from email (simple heuristic)
  function extractFirstName(email) {
    const username = email.split('@')[0];
    // Remove numbers and common separators, capitalize first letter
    const cleanName = username.replace(/[0-9._-]/g, '');
    return cleanName.length > 1 ? cleanName.charAt(0).toUpperCase() + cleanName.slice(1).toLowerCase() : null;
  }

  // Add input event listeners
  emailInput.addEventListener('input', updateSubmitButton);
  consentCheckbox.addEventListener('change', updateSubmitButton);

  // Initial button state
  updateSubmitButton();

  // Form submission with API integration
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = emailInput.value.trim();
    const consent = consentCheckbox.checked;
    
    if (!isValidEmail(email) || !consent) {
      showError('Please enter a valid email and accept the terms.');
      return;
    }

    setLoadingState(true);

    try {
      // Extract potential first name from email
      const firstName = extractFirstName(email);
      
      // Submit to API
      const response = await emailHandler.submitEmail(email, firstName);
      
      console.log('Successfully submitted:', response);
      
      // Launch confetti
      if (typeof launchConfetti === 'function') {
        launchConfetti();
      }
      
      // Animate form out
      form.style.transition = 'all 0.3s ease';
      form.style.opacity = '0';
      form.style.transform = 'translateY(-20px)';
      
      setTimeout(() => {
        // Hide form and show success message
        form.style.display = 'none';
        successMessage.style.display = 'block';
        successMessage.style.opacity = '0';
        successMessage.style.transform = 'translateY(20px)';
        
        // Trigger reflow
        successMessage.offsetHeight;
        
        // Animate in success message
        successMessage.style.transition = 'all 0.3s ease';
        successMessage.style.opacity = '1';
        successMessage.style.transform = 'translateY(0)';
        successMessage.classList.add('visible');
        
        // Update subscriber count in stats if element exists
        updateSubscriberCount();
      }, 300);
      
    } catch (error) {
      console.error('Submission failed:', error);
      setLoadingState(false);
      
      // Show user-friendly error message
      let errorMessage = 'Something went wrong. Please try again.';
      
      if (error.message.includes('No email provided')) {
        errorMessage = 'Please enter a valid email address.';
      } else if (error.message.includes('network') || error.message.includes('fetch')) {
        errorMessage = 'Connection error. Please check your internet and try again.';
      } else if (error.message.includes('500')) {
        errorMessage = 'Server error. Please try again in a moment.';
      }
      
      showError(errorMessage);
    }
  });

  // Function to update subscriber count display
  async function updateSubscriberCount() {
    try {
      const count = await emailHandler.getSubscriberCount();
      const statNumber = document.querySelector('.stat-number');
      if (statNumber && statNumber.textContent !== 'Every' && statNumber.textContent !== '95%') {
        // Animate the number change
        const currentCount = parseInt(statNumber.textContent) || 0;
        const newCount = count;
        
        if (newCount > currentCount) {
          animateCounter(statNumber, currentCount, newCount, 1000);
        }
      }
    } catch (error) {
      console.log('Could not update subscriber count:', error);
    }
  }

  // Counter animation function
  function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    const difference = end - start;
    
    function updateCounter(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function for smooth animation
      const easeOutCubic = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(start + (difference * easeOutCubic));
      
      element.textContent = current;
      
      if (progress < 1) {
        requestAnimationFrame(updateCounter);
      } else {
        element.textContent = end;
      }
    }
    
    requestAnimationFrame(updateCounter);
  }

  // Load initial subscriber count on page load
  updateSubscriberCount();
});

// Export for use in other scripts if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = EmailHandler;
}
