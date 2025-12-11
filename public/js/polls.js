document.addEventListener('DOMContentLoaded', async () => {
  if (!authManager.isAuthenticated()) {
    window.location.href = '/login.html';
    return;
  }

  const user = await authManager.getCurrentUser();
  
  // Show/hide teacher/admin controls
  if (user.data.role === 'teacher' || user.data.role === 'admin') {
    document.querySelectorAll('.teacher-admin-only').forEach(el => el.style.display = 'block');
  }

  loadPolls();

  // Filter listeners
  document.getElementById('statusFilter').addEventListener('change', loadPolls);
  if (document.getElementById('creatorFilter')) {
    document.getElementById('creatorFilter').addEventListener('change', loadPolls);
  }
});

async function loadPolls() {
  const status = document.getElementById('statusFilter').value;
  const creator = document.getElementById('creatorFilter')?.value || '';

  let url = `/api/polls?status=${status}`;
  if (creator) url += `&createdBy=${creator}`;

  try {
    const response = await fetch(url, {
      headers: authManager.getAuthHeaders()
    });

    const result = await response.json();

    if (result.success) {
      displayPolls(result.data);
    } else {
      alert(result.error);
    }
  } catch (error) {
    console.error('Error loading polls:', error);
    alert('Error loading polls');
  }
}

function displayPolls(polls) {
  const container = document.getElementById('pollsList');

  if (polls.length === 0) {
    container.innerHTML = '<p class="no-data">No polls found</p>';
    return;
  }

  container.innerHTML = polls.map(poll => `
    <div class="poll-card ${poll.isExpired ? 'expired' : ''}">
      <h3>${poll.title}</h3>
      <p class="poll-question">${poll.question}</p>
      <p class="poll-meta">
        <span>By: ${poll.createdBy.name}</span>
        <span>Ends: ${new Date(poll.endDate).toLocaleString()}</span>
      </p>
      <p class="poll-status">
        ${poll.hasVoted ? '✓ You voted' : ''}
        ${poll.isExpired ? '⏰ Expired' : '🟢 Active'}
        <span>${poll.totalVotes} vote(s)</span>
      </p>
      <button onclick="viewPoll('${poll._id}')" class="btn-primary">
        ${poll.hasVoted || poll.isExpired ? 'View Results' : 'Vote Now'}
      </button>
    </div>
  `).join('');
}

function viewPoll(pollId) {
  window.location.href = `/poll-details.html?id=${pollId}`;
}
