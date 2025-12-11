import os

def create_directory(path):
    """Create directory if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"✓ Created directory: {path}")

def create_file(filepath, content):
    """Create file with content"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created file: {filepath}")

# Create directory structure
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, 'templates')
admin_dir = os.path.join(templates_dir, 'admin')
voter_dir = os.path.join(templates_dir, 'voter')
static_dir = os.path.join(base_dir, 'static')
css_dir = os.path.join(static_dir, 'css')
js_dir = os.path.join(static_dir, 'js')

for directory in [templates_dir, admin_dir, voter_dir, static_dir, css_dir, js_dir]:
    create_directory(directory)

# Template contents dictionary
templates = {
    'admin/login.html': '''{% extends "base.html" %}
{% block title %}Admin Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0"><i class="bi bi-person-lock"></i> Admin Login</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" name="username" required autofocus>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Login</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'admin/dashboard.html': '''{% extends "base.html" %}
{% block title %}Admin Dashboard{% endblock %}
{% block content %}
<h2><i class="bi bi-speedometer2"></i> Admin Dashboard</h2>
<hr>
<div class="row mb-4">
    <div class="col-md-3">
        <div class="card text-white bg-primary">
            <div class="card-body">
                <h5>Elections</h5>
                <h2>{{ total_elections }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-success">
            <div class="card-body">
                <h5>Candidates</h5>
                <h2>{{ total_candidates }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-info">
            <div class="card-body">
                <h5>Voters</h5>
                <h2>{{ total_voters }}</h2>
            </div>
        </div>
    </div>
    <div class="col-md-3">
        <div class="card text-white bg-warning">
            <div class="card-body">
                <h5>Total Votes</h5>
                <h2>{{ total_votes }}</h2>
            </div>
        </div>
    </div>
</div>
<div class="mb-3">
    <a href="{{ url_for('manage_elections') }}" class="btn btn-primary">Manage Elections</a>
    <a href="{{ url_for('view_all_votes') }}" class="btn btn-info">View All Votes</a>
</div>
<h3>All Elections</h3>
<table class="table table-striped">
    <thead>
        <tr>
            <th>Title</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Status</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        {% for election in elections %}
        <tr>
            <td>{{ election.title }}</td>
            <td>{{ election.start_date.strftime('%Y-%m-%d %H:%M') }}</td>
            <td>{{ election.end_date.strftime('%Y-%m-%d %H:%M') }}</td>
            <td><span class="badge bg-{{ 'success' if election.status == 'active' else 'secondary' }}">{{ election.status }}</span></td>
            <td>
                <a href="{{ url_for('manage_candidates', election_id=election.id) }}" class="btn btn-sm btn-primary">Candidates</a>
                <a href="{{ url_for('view_results', election_id=election.id) }}" class="btn btn-sm btn-info">Results</a>
            </td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% endblock %}''',

    'admin/profile.html': '''{% extends "base.html" %}
{% block title %}Admin Profile{% endblock %}
{% block content %}
<h2>Change Password</h2>
<hr>
<div class="row">
    <div class="col-md-6">
        <form method="POST">
            <div class="mb-3">
                <label for="current_password" class="form-label">Current Password</label>
                <input type="password" class="form-control" id="current_password" name="current_password" required>
            </div>
            <div class="mb-3">
                <label for="new_password" class="form-label">New Password</label>
                <input type="password" class="form-control" id="new_password" name="new_password" required>
            </div>
            <div class="mb-3">
                <label for="confirm_password" class="form-label">Confirm Password</label>
                <input type="password" class="form-control" id="confirm_password" name="confirm_password" required>
            </div>
            <button type="submit" class="btn btn-primary">Change Password</button>
        </form>
    </div>
</div>
{% endblock %}''',

    'voter/register.html': '''{% extends "base.html" %}
{% block title %}Voter Registration{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0">Voter Registration</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="voter_id" class="form-label">Voter ID</label>
                        <input type="text" class="form-control" id="voter_id" name="voter_id" required>
                        <small class="form-text text-muted">5-20 alphanumeric characters</small>
                    </div>
                    <div class="mb-3">
                        <label for="name" class="form-label">Full Name</label>
                        <input type="text" class="form-control" id="name" name="name" required>
                    </div>
                    <div class="mb-3">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" class="form-control" id="email" name="email" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                        <small class="form-text text-muted">Min 8 characters, include letters and numbers</small>
                    </div>
                    <div class="mb-3">
                        <label for="confirm_password" class="form-label">Confirm Password</label>
                        <input type="password" class="form-control" id="confirm_password" name="confirm_password" required>
                    </div>
                    <button type="submit" class="btn btn-success w-100">Register</button>
                    <div class="mt-3 text-center">
                        Already registered? <a href="{{ url_for('voter_login') }}">Login here</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'voter/login.html': '''{% extends "base.html" %}
{% block title %}Voter Login{% endblock %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header bg-success text-white">
                <h4 class="mb-0">Voter Login</h4>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="voter_id" class="form-label">Voter ID</label>
                        <input type="text" class="form-control" id="voter_id" name="voter_id" required autofocus>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <button type="submit" class="btn btn-success w-100">Login</button>
                    <div class="mt-3 text-center">
                        Don't have an account? <a href="{{ url_for('voter_register') }}">Register here</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}''',

    'voter/dashboard.html': '''{% extends "base.html" %}
{% block title %}Voter Dashboard{% endblock %}
{% block content %}
<h2>Welcome, {{ voter.name }}!</h2>
<hr>
<h3>Active Elections</h3>
{% if elections %}
<div class="row">
    {% for election in elections %}
    <div class="col-md-6 mb-3">
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">{{ election.title }}</h5>
                <p class="card-text">{{ election.description or 'No description' }}</p>
                {% if voter.has_voted(election.id) %}
                <span class="badge bg-success">You have voted</span>
                {% else %}
                <a href="{{ url_for('vote', election_id=election.id) }}" class="btn btn-primary">Vote Now</a>
                {% endif %}
            </div>
        </div>
    </div>
    {% endfor %}
</div>
{% else %}
<div class="alert alert-info">No active elections at the moment.</div>
{% endif %}
{% endblock %}''',

    'voter/vote.html': '''{% extends "base.html" %}
{% block title %}Cast Your Vote{% endblock %}
{% block content %}
<h2>{{ election.title }}</h2>
<p class="lead">{{ election.description }}</p>
<hr>
<form method="POST">
    <div class="row">
        {% for candidate in candidates %}
        <div class="col-md-6 mb-3">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">{{ candidate.name }}</h5>
                    <p class="text-muted">{{ candidate.party }}</p>
                    <p>{{ candidate.description or 'No description' }}</p>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="candidate_id" value="{{ candidate.id }}" id="candidate{{ candidate.id }}" required>
                        <label class="form-check-label" for="candidate{{ candidate.id }}">
                            Select this candidate
                        </label>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    <button type="submit" class="btn btn-success btn-lg mt-3" onclick="return confirm('Are you sure? This action cannot be undone.')">Cast My Vote</button>
</form>
{% endblock %}''',
}

# Create all template files
for filepath, content in templates.items():
    full_path = os.path.join(templates_dir, filepath)
    create_file(full_path, content)

print("\n✓ All template files created successfully!")
print("\nRun 'python create_remaining_templates.py' to create the remaining admin templates.")
