# Backend Code Explanation - Flask Application

## 📋 Overview

This document explains the **app.py** file - the heart of the application. It contains all the backend logic, routes, and database operations.

---

## 🏗️ Application Structure

### **1. Imports and Setup**

```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from config import Config
```

**What each import does:**

| Import | Purpose |
|--------|---------|
| `Flask` | Creates the web application |
| `render_template` | Loads HTML files and displays them |
| `request` | Gets data from forms (POST/GET) |
| `redirect` | Sends user to different page |
| `url_for` | Generates URLs for routes |
| `flash` | Shows one-time messages to user |
| `session` | Stores temporary user data |
| `SQLAlchemy` | Database toolkit (ORM) |
| `LoginManager` | Manages user login sessions |
| `UserMixin` | Adds login functionality to models |
| `generate_password_hash` | Encrypts passwords |
| `check_password_hash` | Verifies passwords |
| `datetime` | Works with dates and times |

---

## 🔧 Flask App Initialization

```python
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
```

**Line-by-line explanation:**

```python
app = Flask(__name__)
# Creates a Flask application instance
# __name__ tells Flask where to find templates/static files

app.config.from_object(Config)
# Loads configuration from config.py
# Includes database URL, secret key, etc.

db = SQLAlchemy(app)
# Creates database connection
# Allows us to use Python classes instead of SQL queries

login_manager = LoginManager(app)
# Sets up user session management
# Tracks who is logged in

login_manager.login_view = 'login'
# If user tries to access protected page without logging in
# Redirects them to the 'login' route
```

---

## 🗄️ Database Models Explained

### **1. Admin Model**

```python
class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    elections = db.relationship('Election', backref='creator', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

**Breaking it down:**

```python
class Admin(UserMixin, db.Model):
# UserMixin: Adds login methods (is_authenticated, is_active, etc.)
# db.Model: Makes this a database table

__tablename__ = 'admins'
# Table name in MySQL will be 'admins'

id = db.Column(db.Integer, primary_key=True)
# Auto-incrementing ID number for each admin
# primary_key=True means it's unique and used for lookups

username = db.Column(db.String(80), unique=True, nullable=False)
# String field, max 80 characters
# unique=True: No two admins can have same username
# nullable=False: This field is required

password_hash = db.Column(db.String(255), nullable=False)
# Stores encrypted password (not the actual password!)
# 255 characters to fit the hash

created_at = db.Column(db.DateTime, default=datetime.utcnow)
# Automatically stores when admin was created

elections = db.relationship('Election', backref='creator', lazy=True)
# Links to Election model
# admin.elections gives all elections created by this admin
# election.creator gives the admin who created it

def set_password(self, password):
    self.password_hash = generate_password_hash(password)
# Takes plain password "admin123"
# Converts to "$2b$12$xyz...abc" (encrypted)
# WHY: So if database is hacked, passwords are safe

def check_password(self, password):
    return check_password_hash(self.password_hash, password)
# Compares entered password with stored hash
# Returns True if match, False if not
```

---

### **2. Voter Model**

```python
class Voter(db.Model):
    __tablename__ = 'voters'
    
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    votes = db.relationship('Vote', backref='voter', lazy=True)
```

**Why this model:**
- Separate from Admin (different permissions)
- `voter_id`: Custom ID like "VOTER001" (not database ID)
- `votes` relationship: See all votes by this voter

---

### **3. Election Model**

```python
class Election(db.Model):
    __tablename__ = 'elections'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='upcoming')
    created_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    candidates = db.relationship('Candidate', backref='election', 
                                lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='election', lazy=True)
```

**Key concepts:**

```python
status = db.Column(db.String(20), default='upcoming')
# Can be: 'upcoming', 'active', 'completed'
# Default is 'upcoming' when created

created_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
# Links to Admin table
# Stores which admin created this election

cascade='all, delete-orphan'
# If election is deleted, delete all its candidates too
# Prevents orphaned data
```

---

### **4. Candidate Model**

```python
class Candidate(db.Model):
    __tablename__ = 'candidates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100))
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), 
                           nullable=False)
    
    # Relationships
    votes = db.relationship('Vote', backref='candidate', lazy=True)
```

**Understanding relationships:**

```python
election_id = db.Column(db.Integer, db.ForeignKey('elections.id'))
# Each candidate belongs to ONE election
# Stores the election's ID

votes = db.relationship('Vote', backref='candidate', lazy=True)
# candidate.votes → List of all votes for this candidate
# vote.candidate → Gets the candidate this vote is for
```

---

### **5. Vote Model**

```python
class Vote(db.Model):
    __tablename__ = 'votes'
    
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), 
                        nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), 
                           nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), 
                            nullable=False)
    voted_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**The most important model:**

```python
# Three foreign keys ensure data integrity:
voter_id    → Who voted
election_id → In which election
candidate_id → For which candidate

# Combination ensures:
# - Can't vote for candidate not in that election
# - Can't create fake votes
# - Can track voting patterns (for analytics)
```

---

## 🛣️ Route Functions Explained

### **Homepage Route**

```python
@app.route('/')
def index():
    # Get all active elections
    current_time = datetime.utcnow()
    elections = Election.query.filter(
        Election.start_date <= current_time,
        Election.end_date >= current_time
    ).all()
    
    return render_template('index.html', elections=elections)
```

**What happens:**

```python
@app.route('/')
# Decorator: Tells Flask this function handles the homepage
# When user visits http://localhost:5000/, run this function

def index():
# Function name can be anything
# Used with url_for('index') to generate URLs

current_time = datetime.utcnow()
# Gets current date/time in UTC

Election.query.filter(...)
# Query database for elections where:
# - start_date <= now (already started)
# - end_date >= now (not yet ended)
# Result: Only active elections

return render_template('index.html', elections=elections)
# Loads templates/index.html
# Passes 'elections' variable to template
# Template can use {{ elections }} to display data
```

---

### **Admin Login Route**

```python
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('admin/login.html')
```

**Step-by-step breakdown:**

```python
methods=['GET', 'POST']
# GET: Display the login form
# POST: Process form submission

if request.method == 'POST':
# Only process login if form was submitted

username = request.form.get('username')
# Gets value from <input name="username"> in form

admin = Admin.query.filter_by(username=username).first()
# Searches database for admin with this username
# .first() returns one result (or None if not found)

if admin and admin.check_password(password):
# Check two things:
# 1. Admin exists (admin is not None)
# 2. Password is correct

login_user(admin)
# Creates secure session
# Sets cookie in browser
# Marks user as logged in

flash('Login successful!', 'success')
# Stores message to show on next page
# 'success' is the category (shows as green alert)

return redirect(url_for('admin_dashboard'))
# Sends user to dashboard
# url_for generates URL for 'admin_dashboard' function

return render_template('admin/login.html')
# If GET request or login failed
# Show the login form
```

---

### **Voting Route (Complex Example)**

```python
@app.route('/voter/election/<int:election_id>/vote', methods=['GET', 'POST'])
def cast_vote(election_id):
    # Check if voter is logged in
    if 'voter_id' not in session:
        flash('Please login to vote', 'warning')
        return redirect(url_for('voter_login'))
    
    voter_id = session['voter_id']
    
    # Get election
    election = Election.query.get_or_404(election_id)
    
    # Check if already voted
    existing_vote = Vote.query.filter_by(
        voter_id=voter_id,
        election_id=election_id
    ).first()
    
    if existing_vote:
        flash('You have already voted in this election!', 'warning')
        return redirect(url_for('voter_dashboard'))
    
    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        
        # Create vote
        vote = Vote(
            voter_id=voter_id,
            election_id=election_id,
            candidate_id=candidate_id
        )
        
        db.session.add(vote)
        db.session.commit()
        
        flash('Vote cast successfully!', 'success')
        return redirect(url_for('voter_dashboard'))
    
    # Get candidates
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    return render_template('voter/vote.html', 
                         election=election, 
                         candidates=candidates)
```

**Security features explained:**

```python
if 'voter_id' not in session:
# Ensures voter is logged in
# session is like a dictionary stored in cookie

Election.query.get_or_404(election_id)
# Gets election or shows 404 error if not found
# Prevents voting for non-existent elections

existing_vote = Vote.query.filter_by(...)
# Checks if this voter already voted
# Prevents double voting

db.session.add(vote)
# Adds vote to database transaction

db.session.commit()
# Saves to database permanently
# If error occurs, vote is not saved
```

---

## 🔒 Authentication System

### **User Loader Function**

```python
@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))
```

**Purpose:**
- Flask-Login calls this to reload user from session
- Converts user ID from cookie to actual User object
- Called on every request to protected routes

---

### **Login Required Decorator**

```python
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # This function only runs if user is logged in
    # Otherwise, redirects to login page
```

**How it works:**
1. User tries to access `/admin/dashboard`
2. `@login_required` checks if user is authenticated
3. If yes: Run the function
4. If no: Redirect to `login_manager.login_view` (login page)

---

## 💾 Database Operations

### **Creating Records**

```python
# Create new admin
admin = Admin(
    username='john',
    email='john@example.com'
)
admin.set_password('secret123')

db.session.add(admin)  # Stage for saving
db.session.commit()    # Save to database
```

### **Reading Records**

```python
# Get one record
admin = Admin.query.filter_by(username='john').first()

# Get all records
all_admins = Admin.query.all()

# Get with conditions
active_elections = Election.query.filter(
    Election.status == 'active'
).all()

# Get by ID
election = Election.query.get(5)
```

### **Updating Records**

```python
admin = Admin.query.get(1)
admin.email = 'newemail@example.com'
db.session.commit()  # Save changes
```

### **Deleting Records**

```python
admin = Admin.query.get(1)
db.session.delete(admin)
db.session.commit()
```

---

## 🎯 Key Concepts Summary

### **1. Why Flask?**
- Lightweight and flexible
- Easy to learn
- Perfect for small to medium projects
- Large community and documentation

### **2. Why SQLAlchemy?**
- No need to write SQL queries
- Prevents SQL injection attacks
- Works with multiple databases
- Object-oriented (more Pythonic)

### **3. Why Flask-Login?**
- Handles session management
- Protects routes easily
- Remembers logged-in users
- Industry standard

### **4. Why Password Hashing?**
- Passwords never stored in plain text
- Even if database is leaked, passwords are safe
- One-way encryption (can't reverse)
- Salt prevents rainbow table attacks

---

## 📊 Request-Response Cycle

```
1. User clicks "Login" button
         ↓
2. Browser sends POST request to /admin/login
         ↓
3. Flask receives request
         ↓
4. Route function (@app.route) runs
         ↓
5. Extract username & password from form
         ↓
6. Query database for user
         ↓
7. Check password hash
         ↓
8. If valid: Create session, redirect to dashboard
   If invalid: Show error message
         ↓
9. Flask sends HTML response
         ↓
10. Browser displays page to user
```

---

## 🚀 Advanced Topics

### **Database Migrations**
```python
# When you change models, you need to update database
flask db init       # Initialize migrations
flask db migrate    # Create migration script
flask db upgrade    # Apply changes to database
```

### **Error Handling**
```python
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
```

### **Context Processors**
```python
@app.context_processor
def inject_user():
    return dict(current_time=datetime.utcnow())
# Makes 'current_time' available in all templates
```

---

**Next:** Read [Database Explanation](DATABASE_EXPLANATION.md) for deep dive into database design!
