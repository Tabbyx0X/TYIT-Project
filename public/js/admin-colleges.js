document.getElementById('createCollegeForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const data = {
    name: document.getElementById('collegeName').value,
    code: document.getElementById('collegeCode').value,
    address: document.getElementById('collegeAddress').value
  };

  try {
    const response = await fetch('/api/college/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    if (response.ok) {
      alert('College created successfully!');
      loadColleges();
      e.target.reset();
    } else {
      alert(result.error);
    }
  } catch (error) {
    alert('Error creating college');
  }
});

async function loadColleges() {
  try {
    const response = await fetch('/api/college/list');
    const colleges = await response.json();
    
    const listDiv = document.getElementById('collegesList');
    listDiv.innerHTML = colleges.map(college => `
      <div class="college-card">
        <h3>${college.name}</h3>
        <p><strong>Code:</strong> ${college.code}</p>
        <p>${college.address || ''}</p>
      </div>
    `).join('');
  } catch (error) {
    console.error('Error loading colleges:', error);
  }
}

loadColleges();
