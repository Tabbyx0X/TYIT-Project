# Frontend Explanation - HTML Templates & Jinja2

## 📋 Overview

This document explains how the frontend works, including HTML templates, Jinja2 templating engine, Bootstrap styling, and JavaScript interactions.

---

## 🎨 Frontend Technology Stack

| Technology | Purpose | Why Used |
|------------|---------|----------|
| **HTML5** | Structure | Standard markup language |
| **Bootstrap 5** | Styling | Responsive, professional design |
| **Jinja2** | Templating | Dynamic content generation |
| **JavaScript** | Interactivity | Form validation, AJAX |
| **Font Awesome** | Icons | Beautiful icon library |
| **Chart.js** | Visualization | Election results charts |

---

## 📁 Template Structure

```
templates/
├── base.html              # Master template (all pages inherit)
├── index.html             # Homepage
│
├── admin/
│   ├── login.html         # Admin login page
│   ├── dashboard.html     # Admin dashboard
│   ├── elections.html     # Manage elections
│   ├── add_election.html  # Create new election
│   ├── edit_election.html # Edit election
│   ├── candidates.html    # Manage candidates
│   ├── add_candidate.html # Add new candidate
│   ├── edit_candidate.html# Edit candidate
│   ├── results.html       # View election results
│   └── profile.html       # Admin profile
│
└── voter/
    ├── login.html         # Voter login page
    ├── register.html      # Voter registration
    ├── dashboard.html     # Voter dashboard
    └── vote.html          # Voting page
```

---

## 🏗️ Base Template Explained

### **base.html - The Foundation**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Online Voting System{% endblock %}</title>
    
    <!-- CSS Libraries -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/custom.css') }}">
    
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="{{ url_for('static', filename='images/favicon.svg') }}">
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('index') }}">
                <img src="{{ url_for('static', filename='images/logo.svg') }}" alt="Logo">
                Voting System
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    {% if current_user.is_authenticated %}
                        <!-- Admin Menu -->
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('admin_dashboard') }}">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('logout') }}">Logout</a>
                        </li>
                    {% elif session.get('voter_id') %}
                        <!-- Voter Menu -->
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('voter_dashboard') }}">Dashboard</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('voter_logout') }}">Logout</a>
                        </li>
                    {% else %}
                        <!-- Public Menu -->
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('login') }}">Admin Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('voter_login') }}">Voter Login</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" href="{{ url_for('voter_register') }}">Register</a>
                        </li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>
    
    <!-- Main Content -->
    <div class="content">
        <div class="container mt-4">
            <!-- Flash Messages -->
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <!-- Page Content -->
            {% block content %}{% endblock %}
        </div>
    </div>
    
    <!-- Footer -->
    <footer class="bg-dark text-white text-center py-3 mt-5">
        <div class="container">
            <p class="mb-0">&copy; 2024 Online Voting System. All rights reserved.</p>
        </div>
    </footer>
    
    <!-- JavaScript Libraries -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

---

## 🧩 Jinja2 Templating Engine

### **What is Jinja2?**

Jinja2 is a templating engine that allows you to:
- Insert Python variables into HTML
- Use control structures (if/else, loops)
- Inherit from other templates
- Include reusable components

---

### **1. Template Inheritance**

```html
<!-- Child template extends parent -->
{% extends "base.html" %}

<!-- Override title block -->
{% block title %}Login - Voting System{% endblock %}

<!-- Override content block -->
{% block content %}
    <h1>Login Page</h1>
{% endblock %}
```

**How it works:**
1. `{% extends %}` says "use base.html as foundation"
2. `{% block %}` sections can be overridden
3. Everything not in blocks uses base.html version

**Result:**
```
base.html layout
    ↓
Replace title block → "Login - Voting System"
    ↓
Replace content block → Login form
    ↓
Keep navbar, footer, scripts from base.html
```

---

### **2. Variables**

```html
<!-- From Python: name = "John Doe" -->
<h1>Welcome, {{ name }}!</h1>
<!-- Output: Welcome, John Doe! -->

<!-- Object attributes -->
{{ user.email }}
{{ election.title }}

<!-- Filters -->
{{ name|upper }}  <!-- JOHN DOE -->
{{ date|strftime('%Y-%m-%d') }}  <!-- 2025-01-15 -->
```

**Common Filters:**

| Filter | Example | Output |
|--------|---------|--------|
| `upper` | `{{ "hello"\|upper }}` | HELLO |
| `lower` | `{{ "HELLO"\|lower }}` | hello |
| `title` | `{{ "hello world"\|title }}` | Hello World |
| `length` | `{{ [1,2,3]\|length }}` | 3 |
| `default` | `{{ name\|default('Guest') }}` | Guest (if name is None) |

---

### **3. Control Structures**

#### **If/Else**

```html
{% if user.is_authenticated %}
    <p>Welcome back, {{ user.username }}!</p>
{% elif user.is_guest %}
    <p>Hello, guest!</p>
{% else %}
    <p>Please log in</p>
{% endif %}
```

#### **For Loops**

```html
<!-- Loop through elections list -->
{% for election in elections %}
    <div class="card">
        <h3>{{ election.title }}</h3>
        <p>{{ election.description }}</p>
    </div>
{% endfor %}

<!-- With loop counter -->
{% for candidate in candidates %}
    <p>{{ loop.index }}. {{ candidate.name }}</p>
    <!-- Outputs: 1. John, 2. Jane, 3. Bob -->
{% endfor %}

<!-- Check if empty -->
{% for item in items %}
    <p>{{ item }}</p>
{% else %}
    <p>No items found</p>
{% endfor %}
```

---

### **4. URL Generation**

```html
<!-- Instead of hardcoding: <a href="/admin/dashboard"> -->
<a href="{{ url_for('admin_dashboard') }}">Dashboard</a>

<!-- With parameters -->
<a href="{{ url_for('edit_election', election_id=5) }}">Edit</a>
<!-- Generates: /admin/election/5/edit -->

<!-- For static files -->
<img src="{{ url_for('static', filename='images/logo.svg') }}">
<!-- Generates: /static/images/logo.svg -->
```

**Why use url_for?**
- If you change route URLs, links update automatically
- Handles URL encoding
- Works with blueprints and subdomains

---

### **5. Comments**

```html
{# This is a comment - not visible in HTML output #}

{# 
Multi-line
comment
#}
```

---

## 📄 Page Templates Explained

### **Homepage (index.html)**

```html
{% extends "base.html" %}

{% block title %}Home - Online Voting System{% endblock %}

{% block content %}
<!-- Hero Banner -->
<div class="row mb-5">
    <div class="col-12">
        <img src="{{ url_for('static', filename='images/hero-banner.svg') }}" 
             class="img-fluid rounded" alt="Voting System">
    </div>
</div>

<!-- Welcome Section -->
<div class="row">
    <div class="col-md-12 text-center mb-5">
        <h1 class="display-4">Welcome to Online Voting System</h1>
        <p class="lead">Secure, Transparent, and Easy to Use</p>
    </div>
</div>

<!-- Feature Cards -->
<div class="row mb-5">
    <div class="col-md-4">
        <div class="card text-center h-100">
            <div class="card-body">
                <img src="{{ url_for('static', filename='images/secure-icon.svg') }}" 
                     alt="Secure" style="width: 100px;">
                <h5 class="card-title mt-3">Secure</h5>
                <p class="card-text">Your vote is encrypted and protected.</p>
            </div>
        </div>
    </div>
    <!-- More feature cards... -->
</div>

<!-- Active Elections -->
<div class="row">
    <h2 class="mb-4">Active Elections</h2>
    {% if elections %}
        {% for election in elections %}
            <div class="col-md-6 mb-4">
                <div class="card">
                    <div class="card-body">
                        <h5>{{ election.title }}</h5>
                        <p>{{ election.description or 'No description' }}</p>
                        <span class="badge bg-success">{{ election.status|upper }}</span>
                    </div>
                </div>
            </div>
        {% endfor %}
    {% else %}
        <div class="alert alert-info">
            No active elections at the moment.
        </div>
    {% endif %}
</div>
{% endblock %}
```

**Key concepts:**
- `{% if elections %}`: Check if list has items
- `{% for %}`: Loop through elections
- `{{ election.description or 'No description' }}`: Default value if None
- `|upper` filter: Converts to uppercase

---

### **Login Form (admin/login.html)**

```html
{% extends 'base.html' %}

{% block title %}Admin Login{% endblock %}

{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-6 col-lg-4">
        <div class="card shadow">
            <div class="card-body p-5">
                <!-- Header with Image -->
                <div class="text-center mb-4">
                    <img src="{{ url_for('static', filename='images/admin-login.svg') }}" 
                         style="width: 120px;">
                    <h3>Admin Login</h3>
                </div>
                
                <!-- Login Form -->
                <form method="POST" action="{{ url_for('login') }}">
                    <!-- Username Field -->
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <div class="input-group">
                            <span class="input-group-text">
                                <i class="fas fa-user"></i>
                            </span>
                            <input type="text" 
                                   class="form-control" 
                                   id="username" 
                                   name="username" 
                                   required 
                                   autofocus>
                        </div>
                    </div>
                    
                    <!-- Password Field -->
                    <div class="mb-4">
                        <label for="password" class="form-label">Password</label>
                        <div class="input-group">
                            <span class="input-group-text">
                                <i class="fas fa-lock"></i>
                            </span>
                            <input type="password" 
                                   class="form-control" 
                                   id="password" 
                                   name="password" 
                                   required>
                        </div>
                    </div>
                    
                    <!-- Submit Button -->
                    <button type="submit" class="btn btn-primary w-100">
                        <i class="fas fa-sign-in-alt"></i> Login
                    </button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Form attributes explained:**

```html
<form method="POST" action="{{ url_for('login') }}">
```

- `method="POST"`: Send data securely (not in URL)
- `action`: Where to submit (Flask route)

```html
<input type="text" name="username" required>
```

- `type="text"`: Text input field
- `name="username"`: Key for accessing in Flask (`request.form.get('username')`)
- `required`: HTML5 validation (can't submit empty)
- `autofocus`: Cursor starts here

---

### **Voting Page (voter/vote.html)**

```html
{% extends 'base.html' %}

{% block title %}Cast Vote - {{ election.title }}{% endblock %}

{% block extra_css %}
<style>
    .candidate-card {
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .candidate-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .candidate-card.selected {
        border: 2px solid #0d6efd;
        background-color: #eff6ff;
    }
</style>
{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-10">
        <!-- Election Info -->
        <div class="card mb-4">
            <div class="card-header bg-primary text-white">
                <h4><i class="fas fa-vote-yea"></i> Cast Your Vote</h4>
            </div>
            <div class="card-body">
                <h5>{{ election.title }}</h5>
                <p>{{ election.description }}</p>
                <div class="alert alert-warning">
                    <strong>Important:</strong> You can only vote once!
                </div>
            </div>
        </div>
        
        <!-- Voting Form -->
        <form method="POST" id="voteForm">
            <div class="row">
                {% for candidate in candidates %}
                <div class="col-md-6 mb-4">
                    <div class="card candidate-card" 
                         onclick="selectCandidate({{ candidate.id }})">
                        <div class="card-body">
                            <!-- Radio Button -->
                            <input type="radio" 
                                   name="candidate_id" 
                                   value="{{ candidate.id }}" 
                                   id="candidate_{{ candidate.id }}" 
                                   required>
                            
                            <!-- Candidate Photo -->
                            <img src="{{ candidate.photo_url or url_for('static', filename='images/default-avatar.svg') }}" 
                                 class="rounded-circle" 
                                 style="width: 80px; height: 80px;">
                            
                            <!-- Candidate Info -->
                            <h5>{{ candidate.name }}</h5>
                            {% if candidate.party %}
                                <p><i class="fas fa-flag"></i> {{ candidate.party }}</p>
                            {% endif %}
                            <p>{{ candidate.description }}</p>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <!-- Submit Button -->
            <div class="text-center mt-4">
                <button type="submit" class="btn btn-primary btn-lg">
                    <i class="fas fa-check-circle"></i> Cast Vote
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
function selectCandidate(candidateId) {
    // Remove 'selected' class from all cards
    document.querySelectorAll('.candidate-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // Check the radio button
    document.getElementById('candidate_' + candidateId).checked = true;
    
    // Add 'selected' class to clicked card
    event.currentTarget.classList.add('selected');
}

// Confirm before submission
document.getElementById('voteForm').addEventListener('submit', function(e) {
    if (!confirm('Are you sure you want to cast this vote? This action cannot be undone.')) {
        e.preventDefault();
    }
});
</script>
{% endblock %}
```

**JavaScript explained:**

```javascript
function selectCandidate(candidateId) {
    // 1. Remove previous selection
    document.querySelectorAll('.candidate-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    // 2. Check the radio button
    document.getElementById('candidate_' + candidateId).checked = true;
    
    // 3. Highlight selected card
    event.currentTarget.classList.add('selected');
}
```

**Form validation:**

```javascript
document.getElementById('voteForm').addEventListener('submit', function(e) {
    if (!confirm('Are you sure?')) {
        e.preventDefault();  // Stop form submission
    }
});
```

---

## 🎨 Bootstrap Components Used

### **1. Grid System**

```html
<div class="container">
    <div class="row">
        <div class="col-md-6">Left column</div>
        <div class="col-md-6">Right column</div>
    </div>
</div>
```

**Breakdown:**
- `container`: Centers content, adds padding
- `row`: Horizontal grouping
- `col-md-6`: Takes 6/12 columns (50%) on medium+ screens

---

### **2. Cards**

```html
<div class="card">
    <div class="card-header">Title</div>
    <div class="card-body">
        <h5 class="card-title">Card Title</h5>
        <p class="card-text">Card content</p>
    </div>
    <div class="card-footer">Footer</div>
</div>
```

---

### **3. Alerts**

```html
<div class="alert alert-success">Success message</div>
<div class="alert alert-danger">Error message</div>
<div class="alert alert-warning">Warning message</div>
<div class="alert alert-info">Info message</div>
```

---

### **4. Buttons**

```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-lg">Large button</button>
<button class="btn btn-sm">Small button</button>
```

---

## 🔧 Flash Messages System

### **In Flask (Python)**

```python
from flask import flash

# Success message
flash('Login successful!', 'success')

# Error message
flash('Invalid credentials', 'danger')

# Warning
flash('Account will expire soon', 'warning')

# Info
flash('Please verify your email', 'info')
```

### **In Template (HTML)**

```html
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }} alert-dismissible fade show">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

**How it works:**
1. Flask stores messages in session
2. Template retrieves and displays them
3. Messages are automatically cleared after display
4. Each message has a category (maps to Bootstrap alert classes)

---

## 📊 Chart.js Integration (results.html)

```html
{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
// Data from Flask (converted to JSON)
const labels = {{ labels|tojson }};  // ['John', 'Jane', 'Bob']
const data = {{ data|tojson }};      // [150, 200, 100]

// Create bar chart
const ctx = document.getElementById('resultsChart').getContext('2d');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Votes',
            data: data,
            backgroundColor: ['#0d6efd', '#198754', '#ffc107']
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
</script>
{% endblock %}
```

**Python to JavaScript:**

```python
# In Flask route
labels = ['John', 'Jane', 'Bob']
data = [150, 200, 100]

return render_template('results.html', 
                      labels=labels, 
                      data=data)
```

```html
<!-- In template -->
const labels = {{ labels|tojson }};
// Becomes: const labels = ["John", "Jane", "Bob"];
```

---

## 🎯 Best Practices

### **1. DRY (Don't Repeat Yourself)**

✅ **Good:**
```html
<!-- base.html -->
<nav>...</nav>

<!-- All other pages inherit -->
{% extends "base.html" %}
```

❌ **Bad:**
```html
<!-- Copy navbar to every page -->
```

---

### **2. Secure Forms**

```html
<!-- Always use POST for sensitive data -->
<form method="POST">
    <!-- Include CSRF token (if using Flask-WTF) -->
    {{ form.csrf_token }}
    ...
</form>
```

---

### **3. Accessibility**

```html
<!-- Use semantic HTML -->
<button type="submit">Submit</button>  <!-- Not <div onclick> -->

<!-- Add labels for screen readers -->
<label for="username">Username</label>
<input id="username" name="username">

<!-- Alt text for images -->
<img src="logo.svg" alt="Voting System Logo">
```

---

## 🎓 Summary

**Key Concepts:**
1. **Template Inheritance** reduces code duplication
2. **Jinja2 Variables** connect Python to HTML
3. **Control Structures** enable dynamic content
4. **Bootstrap** provides professional styling
5. **Flash Messages** give user feedback
6. **Form Handling** collects user input
7. **JavaScript** adds interactivity

---

**Next:** Read [Authentication Explanation](AUTHENTICATION_EXPLANATION.md) to learn about security!
