document.addEventListener('DOMContentLoaded', async () => {
  if (!authManager.isAuthenticated()) {
    window.location.href = '/login.html';
    return;
  }

  const user = await authManager.getCurrentUser();
  if (user.data.role !== 'teacher' && user.data.role !== 'admin') {
    alert('Only teachers and admins can create polls');
    window.location.href = '/dashboard.html';
    return;
  }

  // Set minimum end date to current time
  const now = new Date();
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
  document.getElementById('endDate').min = now.toISOString().slice(0, 16);

  // Add option functionality
  document.getElementById('addOption').addEventListener('click', () => {
    const container = document.getElementById('optionsContainer');
    const optionCount = container.querySelectorAll('.poll-option').length;
    
    if (optionCount >= 10) {
      alert('Maximum 10 options allowed');
      return;
    }

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'poll-option';
    input.placeholder = `Option ${optionCount + 1}`;
    input.required = true;

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.textContent = '×';
    removeBtn.className = 'remove-option';
    removeBtn.onclick = () => {
      input.remove();
      removeBtn.remove();
    };

    container.appendChild(input);
    container.appendChild(removeBtn);
  });

  // Form submission
  document.getElementById('createPollForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const options = Array.from(document.querySelectorAll('.poll-option'))
      .map(input => input.value.trim())
      .filter(val => val);

    if (options.length < 2) {
      alert('Please provide at least 2 options');
      return;
    }

    const pollData = {
      title: document.getElementById('title').value.trim(),
      description: document.getElementById('description').value.trim(),
      question: document.getElementById('question').value.trim(),
      options: options,
      pollType: document.getElementById('pollType').value,
      endDate: document.getElementById('endDate').value,
      allowAnonymous: document.getElementById('allowAnonymous').checked,
      targetAudience: {
        department: document.getElementById('department').value.trim()
      },
      settings: {
        showResults: document.getElementById('showResults').value,
        allowChangeVote: document.getElementById('allowChangeVote').checked
      }
    };

    try {
      const response = await fetch('/api/polls', {
        method: 'POST',
        headers: authManager.getAuthHeaders(),
        body: JSON.stringify(pollData)
      });

      const result = await response.json();

      if (result.success) {
        alert('Poll created successfully!');
        window.location.href = '/polls.html';
      } else {
        alert(result.error || 'Failed to create poll');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error creating poll');
    }
  });
});
