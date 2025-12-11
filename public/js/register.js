document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registerForm');
  const collegeCodeInput = document.getElementById('collegeCode');
  const collegeNameDisplay = document.getElementById('collegeName');
  const submitBtn = document.getElementById('submitBtn');
  
  let collegeVerified = false;

  // Real-time college code verification
  let debounceTimer;
  collegeCodeInput.addEventListener('input', async (e) => {
    clearTimeout(debounceTimer);
    const code = e.target.value.trim();

    if (code.length < 4) {
      collegeNameDisplay.textContent = '';
      collegeVerified = false;
      return;
    }

    collegeNameDisplay.textContent = 'Verifying...';
    collegeNameDisplay.className = 'text-info';

    debounceTimer = setTimeout(async () => {
      try {
        const result = await authManager.verifyCollegeCode(code);
        
        if (result.success && result.data.valid) {
          collegeNameDisplay.textContent = `✓ ${result.data.collegeName}`;
          collegeNameDisplay.className = 'text-success';
          collegeVerified = true;
          
          if (!result.data.allowRegistration) {
            collegeNameDisplay.textContent += ' (Registration disabled)';
            collegeNameDisplay.className = 'text-warning';
            collegeVerified = false;
          }
        } else {
          collegeNameDisplay.textContent = '✗ Invalid college code';
          collegeNameDisplay.className = 'text-danger';
          collegeVerified = false;
        }
      } catch (error) {
        collegeNameDisplay.textContent = '✗ Error verifying code';
        collegeNameDisplay.className = 'text-danger';
        collegeVerified = false;
      }
    }, 500);
  });

  // Password strength indicator
  const passwordInput = document.getElementById('password');
  const strengthIndicator = document.getElementById('passwordStrength');
  
  passwordInput.addEventListener('input', (e) => {
    const password = e.target.value;
    let strength = 0;
    
    if (password.length >= 6) strength++;
    if (password.length >= 10) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[^a-zA-Z\d]/.test(password)) strength++;

    const strengths = ['Weak', 'Fair', 'Good', 'Strong', 'Very Strong'];
    const colors = ['#dc3545', '#ffc107', '#17a2b8', '#28a745', '#28a745'];
    
    strengthIndicator.textContent = `Password Strength: ${strengths[strength]}`;
    strengthIndicator.style.color = colors[strength];
  });

  // Form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (!collegeVerified) {
      showNotification('Please enter a valid college code', 'error');
      return;
    }

    const formData = {
      name: document.getElementById('name').value.trim(),
      email: document.getElementById('email').value.trim(),
      password: document.getElementById('password').value,
      collegeCode: document.getElementById('collegeCode').value.trim().toUpperCase(),
      department: document.getElementById('department')?.value,
      phoneNumber: document.getElementById('phoneNumber')?.value
    };

    // Disable submit button
    submitBtn.disabled = true;
    submitBtn.textContent = 'Registering...';

    try {
      const result = await authManager.register(formData);
      
      showNotification(result.message || 'Registration successful!', 'success');
      
      setTimeout(() => {
        window.location.href = '/dashboard.html';
      }, 1500);
    } catch (error) {
      showNotification(error.message || 'Registration failed', 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Register';
    }
  });
});

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.classList.add('show');
  }, 10);

  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}
