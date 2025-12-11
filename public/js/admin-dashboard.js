document.addEventListener('DOMContentLoaded', async () => {
  if (!authManager.isAuthenticated()) {
    window.location.href = '/login.html';
    return;
  }

  try {
    const user = await authManager.getCurrentUser();
    
    if (user.data.role !== 'admin') {
      window.location.href = '/dashboard.html';
      return;
    }

    // Load system-wide statistics
    await loadSystemStats();
    await loadAllColleges();
    await loadAllUsers();
  } catch (error) {
    console.error('Error loading admin dashboard:', error);
    showNotification('Error loading dashboard', 'error');
  }
});

async function loadSystemStats() {
  try {
    const response = await fetch('/api/college/list?limit=1000', {
      headers: authManager.getAuthHeaders()
    });
    
    const result = await response.json();
    
    if (result.success) {
      document.getElementById('totalColleges').textContent = result.pagination.total;
      
      // Calculate total users across all colleges
      const usersResponse = await fetch('/api/users?limit=1000', {
        headers: authManager.getAuthHeaders()
      });
      const usersResult = await usersResponse.json();
      
      if (usersResult.success) {
        const totalUsers = usersResult.pagination.total;
        const totalStudents = usersResult.data.filter(u => u.role === 'student').length;
        const totalTeachers = usersResult.data.filter(u => u.role === 'teacher').length;
        
        document.getElementById('totalUsers').textContent = totalUsers;
        document.getElementById('totalStudents').textContent = totalStudents;
        document.getElementById('totalTeachers').textContent = totalTeachers;
      }
    }
  } catch (error) {
    console.error('Error loading stats:', error);
  }
}

async function loadAllColleges() {
  try {
    const response = await fetch('/api/college/list', {
      headers: authManager.getAuthHeaders()
    });
    
    const result = await response.json();
    
    if (result.success) {
      const collegesContainer = document.getElementById('collegesList');
      collegesContainer.innerHTML = result.data.map(college => `
        <div class="college-card">
          <h3>${college.name}</h3>
          <p><strong>Code:</strong> ${college.code}</p>
          <p><strong>Students:</strong> ${college.statistics.totalStudents}</p>
          <p><strong>Teachers:</strong> ${college.statistics.totalTeachers}</p>
          <p><strong>Status:</strong> ${college.isActive ? '✅ Active' : '❌ Inactive'}</p>
          <button onclick="viewCollege('${college._id}')">View Details</button>
          <button onclick="editCollege('${college._id}')">Edit</button>
        </div>
      `).join('');
    }
  } catch (error) {
    console.error('Error loading colleges:', error);
  }
}

async function loadAllUsers() {
  // Load users from all colleges
  try {
    const response = await fetch('/api/users?page=1&limit=50', {
      headers: authManager.getAuthHeaders()
    });
    
    const result = await response.json();
    
    if (result.success) {
      const usersContainer = document.getElementById('recentUsers');
      usersContainer.innerHTML = result.data.slice(0, 10).map(user => `
        <div class="user-item">
          <span>${user.name} (${user.role})</span>
          <span>${user.collegeId?.name || 'N/A'}</span>
          <span>${user.email}</span>
        </div>
      `).join('');
    }
  } catch (error) {
    console.error('Error loading users:', error);
  }
}

function viewCollege(collegeId) {
  window.location.href = `/college-details.html?id=${collegeId}`;
}

function editCollege(collegeId) {
  window.location.href = `/edit-college.html?id=${collegeId}`;
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  document.body.appendChild(notification);
  setTimeout(() => notification.classList.add('show'), 10);
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}
