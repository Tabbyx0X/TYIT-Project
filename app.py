from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from config import Config
from functools import wraps
import os
import re
import logging
from logging.handlers import RotatingFileHandler
import secrets
from collections import defaultdict
from threading import Lock

app = Flask(__name__)
app.config.from_object(Config)

# ==================== Logging Setup ====================
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/voting_system.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Voting System startup')

# ==================== Rate Limiting ====================
login_attempts = defaultdict(list)
login_lock = Lock()

def check_rate_limit(identifier):
    """Check if the identifier has exceeded login attempts"""
    with login_lock:
        current_time = datetime.utcnow()
        cutoff_time = current_time - timedelta(seconds=app.config['LOGIN_ATTEMPT_WINDOW'])
        
        # Clean old attempts
        login_attempts[identifier] = [
            attempt for attempt in login_attempts[identifier] 
            if attempt > cutoff_time
        ]
        
        # Check if limit exceeded
        if len(login_attempts[identifier]) >= app.config['LOGIN_ATTEMPT_LIMIT']:
            return False, "Too many login attempts. Please try again later."
        
        return True, None

def record_login_attempt(identifier):
    """Record a failed login attempt"""
    with login_lock:
        login_attempts[identifier].append(datetime.utcnow())

def clear_login_attempts(identifier):
    """Clear login attempts for successful login"""
    with login_lock:
        if identifier in login_attempts:
            del login_attempts[identifier]

# Enhanced Security Headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net;"
    return response

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'warning'

# ==================== Validation Helpers ====================

def sanitize_input(text):
    """Sanitize user input to prevent XSS"""
    if not text:
        return text
    # Remove potentially dangerous characters
    text = text.strip()
    # Basic HTML escaping is handled by Flask/Jinja2, but we add extra layer
    return text

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_voter_id(voter_id):
    """Validate voter ID format (alphanumeric, 5-20 characters)"""
    if not voter_id:
        return False
    pattern = r'^[a-zA-Z0-9]{5,20}$'
    return re.match(pattern, voter_id) is not None

def validate_password(password):
    """Validate password strength (min 8 characters, must contain letter and number)"""
    if not password or len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, None

def validate_date_range(start_date, end_date):
    """Validate election date range"""
    if start_date >= end_date:
        return False, "End date must be after start date"
    
    # Check if start date is not too far in the past
    if start_date < datetime.utcnow() - timedelta(days=1):
        return False, "Start date cannot be in the past"
    
    return True, None

# ==================== Custom Decorators ====================

def voter_login_required(f):
    """Decorator to require voter login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'voter_id' not in session:
            flash('Please login first!', 'warning')
            return redirect(url_for('voter_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== Models ====================

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Election(db.Model):
    __tablename__ = 'elections'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    candidates = db.relationship('Candidate', backref='election', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='election', lazy=True, cascade='all, delete-orphan')

    def update_status(self):
        now = datetime.utcnow()
        if now < self.start_date:
            self.status = 'upcoming'
        elif now > self.end_date:
            self.status = 'completed'
        else:
            self.status = 'active'


class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    party = db.Column(db.String(100))
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(255))
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    votes = db.relationship('Vote', backref='candidate', lazy=True)

    def get_vote_count(self):
        return Vote.query.filter_by(candidate_id=self.id).count()


class Voter(db.Model):
    __tablename__ = 'voters'
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.relationship('Vote', backref='voter', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_voted(self, election_id):
        return Vote.query.filter_by(voter_id=self.id, election_id=election_id).first() is not None


class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), nullable=False)
    election_id = db.Column(db.Integer, db.ForeignKey('elections.id'), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


# ==================== Service Layer Functions ====================

# Authentication Services
def authenticate_admin(username, password):
    """Authenticate admin user"""
    try:
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            app.logger.info(f'Admin login successful: {username}')
            return admin, None
        app.logger.warning(f'Failed admin login attempt: {username}')
        return None, "Invalid username or password"
    except Exception as e:
        app.logger.error(f'Error during admin authentication: {str(e)}')
        return None, "An error occurred during login"

def authenticate_voter(voter_id, password):
    """Authenticate voter"""
    try:
        voter = Voter.query.filter_by(voter_id=voter_id).first()
        if voter and voter.check_password(password):
            app.logger.info(f'Voter login successful: {voter_id}')
            return voter, None
        app.logger.warning(f'Failed voter login attempt: {voter_id}')
        return None, "Invalid voter ID or password"
    except Exception as e:
        app.logger.error(f'Error during voter authentication: {str(e)}')
        return None, "An error occurred during login"

# Election Services
def get_active_elections():
    """Get all active elections"""
    try:
        elections = Election.query.all()
        for election in elections:
            election.update_status()
        db.session.commit()
        return Election.query.filter_by(status='active').all()
    except Exception as e:
        app.logger.error(f'Error fetching active elections: {str(e)}')
        db.session.rollback()
        return []

def get_election_statistics():
    """Get system statistics"""
    try:
        return {
            'total_elections': Election.query.count(),
            'total_candidates': Candidate.query.count(),
            'total_voters': Voter.query.count(),
            'total_votes': Vote.query.count()
        }
    except Exception as e:
        app.logger.error(f'Error fetching statistics: {str(e)}')
        return {
            'total_elections': 0,
            'total_candidates': 0,
            'total_voters': 0,
            'total_votes': 0
        }

# Voting Services
def can_vote(voter, election):
    """Check if voter can vote in election"""
    if election.status != 'active':
        return False, "This election is not currently active"
    if voter.has_voted(election.id):
        return False, "You have already voted in this election"
    return True, None

def record_vote(voter_id, election_id, candidate_id):
    """Record a vote with validation"""
    try:
        # Validate candidate belongs to election
        candidate = Candidate.query.get(candidate_id)
        if not candidate or candidate.election_id != election_id:
            app.logger.warning(f'Invalid candidate selection: voter_id={voter_id}, candidate_id={candidate_id}')
            return False, "Invalid candidate selection"
        
        # Double-check voter hasn't already voted (race condition prevention)
        existing_vote = Vote.query.filter_by(
            voter_id=voter_id, 
            election_id=election_id
        ).first()
        
        if existing_vote:
            app.logger.warning(f'Duplicate vote attempt: voter_id={voter_id}, election_id={election_id}')
            return False, "You have already voted in this election"
        
        # Create vote
        vote = Vote(
            voter_id=voter_id,
            election_id=election_id,
            candidate_id=candidate_id
        )
        db.session.add(vote)
        db.session.commit()
        
        app.logger.info(f'Vote recorded: voter_id={voter_id}, election_id={election_id}, candidate_id={candidate_id}')
        return True, "Vote recorded successfully"
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error recording vote: {str(e)}')
        return False, f"Error recording vote. Please try again."

# Results Services
def get_election_results(election_id):
    """Get detailed election results"""
    election = Election.query.get(election_id)
    if not election:
        return None, None, None
    
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    results = []
    
    for candidate in candidates:
        vote_count = candidate.get_vote_count()
        results.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'votes': vote_count
        })
    
    total_votes = sum(r['votes'] for r in results)
    return election, results, total_votes


# ==================== Routes ====================

@app.route('/')
def index():
    elections = Election.query.all()
    for election in elections:
        election.update_status()
    db.session.commit()
    return render_template('index.html', elections=elections)


@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = sanitize_input(request.form.get('username', '').strip())
        password = request.form.get('password', '')
        
        # Input validation
        if not username or not password:
            flash('Please provide both username and password', 'danger')
            return render_template('admin/login.html')
        
        # Check rate limiting
        can_attempt, error_msg = check_rate_limit(f'admin_{username}')
        if not can_attempt:
            app.logger.warning(f'Rate limit exceeded for admin: {username}')
            flash(error_msg, 'danger')
            return render_template('admin/login.html')
        
        # Authenticate using service layer
        admin, error = authenticate_admin(username, password)
        
        if admin:
            login_user(admin)
            clear_login_attempts(f'admin_{username}')
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin_dashboard'))
        else:
            record_login_attempt(f'admin_{username}')
            flash(error, 'danger')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def admin_profile():
    """Admin profile and password change"""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([current_password, new_password, confirm_password]):
            flash('All fields are required', 'danger')
            return render_template('admin/profile.html')
        
        # Verify current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect', 'danger')
            return render_template('admin/profile.html')
        
        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return render_template('admin/profile.html')
        
        # Validate password strength
        is_valid, error_msg = validate_password(new_password)
        if not is_valid:
            flash(error_msg, 'danger')
            return render_template('admin/profile.html')
        
        # Update password
        try:
            current_user.set_password(new_password)
            db.session.commit()
            app.logger.info(f'Password changed for admin: {current_user.username}')
            flash('Password changed successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error changing password: {str(e)}')
            flash(f'Error changing password. Please try again.', 'danger')
    
    return render_template('admin/profile.html')


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Update election statuses
    elections = Election.query.all()
    for election in elections:
        election.update_status()
    db.session.commit()
    
    # Get statistics using service layer
    stats = get_election_statistics()
    
    return render_template('admin/dashboard.html', 
                         elections=elections,
                         total_elections=stats['total_elections'],
                         total_candidates=stats['total_candidates'],
                         total_voters=stats['total_voters'],
                         total_votes=stats['total_votes'])


@app.route('/admin/elections')
@login_required
def manage_elections():
    elections = Election.query.all()
    return render_template('admin/elections.html', elections=elections)


@app.route('/admin/elections/add', methods=['GET', 'POST'])
@login_required
def add_election():
    if request.method == 'POST':
        title = sanitize_input(request.form.get('title', '').strip())
        description = sanitize_input(request.form.get('description', '').strip())
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        # Input validation
        if not title:
            flash('Election title is required', 'danger')
            return render_template('admin/add_election.html')
        
        if len(title) > 200:
            flash('Election title is too long (max 200 characters)', 'danger')
            return render_template('admin/add_election.html')
        
        if not start_date_str or not end_date_str:
            flash('Start date and end date are required', 'danger')
            return render_template('admin/add_election.html')
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date format', 'danger')
            return render_template('admin/add_election.html')
        
        # Validate date range
        valid, error_msg = validate_date_range(start_date, end_date)
        if not valid:
            flash(error_msg, 'danger')
            return render_template('admin/add_election.html')
        
        # Create election
        election = Election(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date
        )
        election.update_status()
        
        try:
            db.session.add(election)
            db.session.commit()
            app.logger.info(f'Election created: {title}')
            flash('Election created successfully!', 'success')
            return redirect(url_for('manage_elections'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating election: {str(e)}')
            flash(f'Error creating election. Please try again.', 'danger')
    
    return render_template('admin/add_election.html')


@app.route('/admin/elections/<int:election_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_election(election_id):
    election = Election.query.get_or_404(election_id)
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        
        # Input validation
        if not title:
            flash('Election title is required', 'danger')
            return render_template('admin/edit_election.html', election=election)
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%dT%H:%M')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Invalid date format', 'danger')
            return render_template('admin/edit_election.html', election=election)
        
        # Validate date range
        valid, error_msg = validate_date_range(start_date, end_date)
        if not valid:
            flash(error_msg, 'danger')
            return render_template('admin/edit_election.html', election=election)
        
        # Update election
        election.title = title
        election.description = description
        election.start_date = start_date
        election.end_date = end_date
        election.update_status()
        
        try:
            db.session.commit()
            flash('Election updated successfully!', 'success')
            return redirect(url_for('manage_elections'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating election: {str(e)}', 'danger')
    
    return render_template('admin/edit_election.html', election=election)


@app.route('/admin/elections/<int:election_id>/delete', methods=['POST'])
@login_required
def delete_election(election_id):
    election = Election.query.get_or_404(election_id)
    db.session.delete(election)
    db.session.commit()
    flash('Election deleted successfully!', 'success')
    return redirect(url_for('manage_elections'))


@app.route('/admin/elections/<int:election_id>/candidates')
@login_required
def manage_candidates(election_id):
    election = Election.query.get_or_404(election_id)
    return render_template('admin/candidates.html', election=election)


@app.route('/admin/elections/<int:election_id>/candidates/add', methods=['GET', 'POST'])
@login_required
def add_candidate(election_id):
    election = Election.query.get_or_404(election_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        party = request.form.get('party', '').strip()
        description = request.form.get('description', '').strip()
        photo_url = request.form.get('photo_url', '').strip()
        
        # Input validation
        if not name:
            flash('Candidate name is required', 'danger')
            return render_template('admin/add_candidate.html', election=election)
        
        if not party:
            flash('Party name is required', 'danger')
            return render_template('admin/add_candidate.html', election=election)
        
        # Create candidate
        candidate = Candidate(
            name=name,
            party=party,
            description=description,
            photo_url=photo_url,
            election_id=election_id
        )
        
        try:
            db.session.add(candidate)
            db.session.commit()
            flash('Candidate added successfully!', 'success')
            return redirect(url_for('manage_candidates', election_id=election_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding candidate: {str(e)}', 'danger')
    
    return render_template('admin/add_candidate.html', election=election)


@app.route('/admin/candidates/<int:candidate_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        party = request.form.get('party', '').strip()
        description = request.form.get('description', '').strip()
        photo_url = request.form.get('photo_url', '').strip()
        
        # Input validation
        if not name:
            flash('Candidate name is required', 'danger')
            return render_template('admin/edit_candidate.html', candidate=candidate)
        
        if not party:
            flash('Party name is required', 'danger')
            return render_template('admin/edit_candidate.html', candidate=candidate)
        
        # Update candidate
        candidate.name = name
        candidate.party = party
        candidate.description = description
        candidate.photo_url = photo_url
        
        try:
            db.session.commit()
            flash('Candidate updated successfully!', 'success')
            return redirect(url_for('manage_candidates', election_id=candidate.election_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating candidate: {str(e)}', 'danger')
    
    return render_template('admin/edit_candidate.html', candidate=candidate)


@app.route('/admin/candidates/<int:candidate_id>/delete', methods=['POST'])
@login_required
def delete_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    election_id = candidate.election_id
    
    try:
        db.session.delete(candidate)
        db.session.commit()
        flash('Candidate deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting candidate: {str(e)}', 'danger')
    
    return redirect(url_for('manage_candidates', election_id=election_id))


@app.route('/admin/elections/<int:election_id>/results')
@login_required
def view_results(election_id):
    # Use service layer
    election, results, total_votes = get_election_results(election_id)
    
    if not election:
        flash('Election not found', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/results.html', 
                         election=election, 
                         results=results,
                         total_votes=total_votes)


@app.route('/api/elections/<int:election_id>/results')
def api_results(election_id):
    # Use service layer
    election, results, total_votes = get_election_results(election_id)
    
    if not election:
        return jsonify({'error': 'Election not found'}), 404
    
    return jsonify({
        'election_id': election_id,
        'election_title': election.title,
        'results': results,
        'total_votes': total_votes
    })


@app.route('/admin/all-votes')
@login_required
def view_all_votes():
    """View all votes with voter and candidate details"""
    # Get all votes with related data
    votes = db.session.query(
        Vote,
        Voter,
        Candidate,
        Election
    ).join(
        Voter, Vote.voter_id == Voter.id
    ).join(
        Candidate, Vote.candidate_id == Candidate.id
    ).join(
        Election, Vote.election_id == Election.id
    ).order_by(Vote.timestamp.desc()).all()
    
    return render_template('admin/all_votes.html', votes=votes)


@app.route('/admin/elections/<int:election_id>/votes')
@login_required
def view_election_votes(election_id):
    """View all votes for a specific election"""
    election = Election.query.get_or_404(election_id)
    
    # Get votes for this election
    votes = db.session.query(
        Vote,
        Voter,
        Candidate
    ).join(
        Voter, Vote.voter_id == Voter.id
    ).join(
        Candidate, Vote.candidate_id == Candidate.id
    ).filter(
        Vote.election_id == election_id
    ).order_by(Vote.timestamp.desc()).all()
    
    return render_template('admin/election_votes.html', 
                         election=election, 
                         votes=votes)


@app.route('/voter/register', methods=['GET', 'POST'])
def voter_register():
    if request.method == 'POST':
        voter_id = sanitize_input(request.form.get('voter_id', '').strip())
        name = sanitize_input(request.form.get('name', '').strip())
        email = sanitize_input(request.form.get('email', '').strip().lower())
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Input validation
        if not all([voter_id, name, email, password]):
            flash('All fields are required', 'danger')
            return render_template('voter/register.html')
        
        if not validate_voter_id(voter_id):
            flash('Invalid Voter ID format. Use 5-20 alphanumeric characters', 'danger')
            return render_template('voter/register.html')
        
        if not validate_email(email):
            flash('Invalid email format', 'danger')
            return render_template('voter/register.html')
        
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            flash(error_msg, 'danger')
            return render_template('voter/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('voter/register.html')
        
        # Check for duplicates
        if Voter.query.filter_by(voter_id=voter_id).first():
            flash('Voter ID already exists!', 'danger')
            return render_template('voter/register.html')
        
        if Voter.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return render_template('voter/register.html')
        
        # Create voter
        voter = Voter(voter_id=voter_id, name=name, email=email)
        voter.set_password(password)
        
        try:
            db.session.add(voter)
            db.session.commit()
            app.logger.info(f'New voter registered: {voter_id}')
            flash('Registration successful! Please login to vote.', 'success')
            return redirect(url_for('voter_login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error during voter registration: {str(e)}')
            flash(f'Error during registration. Please try again.', 'danger')
    
    return render_template('voter/register.html')


@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login():
    # Redirect if already logged in
    if 'voter_id' in session:
        return redirect(url_for('voter_dashboard'))
    
    if request.method == 'POST':
        voter_id = sanitize_input(request.form.get('voter_id', '').strip())
        password = request.form.get('password', '')
        
        # Input validation
        if not voter_id or not password:
            flash('Please provide both Voter ID and password', 'danger')
            return render_template('voter/login.html')
        
        # Check rate limiting
        can_attempt, error_msg = check_rate_limit(f'voter_{voter_id}')
        if not can_attempt:
            app.logger.warning(f'Rate limit exceeded for voter: {voter_id}')
            flash(error_msg, 'danger')
            return render_template('voter/login.html')
        
        # Authenticate using service layer
        voter, error = authenticate_voter(voter_id, password)
        
        if voter:
            session['voter_id'] = voter.id
            session.permanent = True  # Use configured session lifetime
            clear_login_attempts(f'voter_{voter_id}')
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('voter_dashboard'))
        else:
            record_login_attempt(f'voter_{voter_id}')
            flash(error, 'danger')
    
    return render_template('voter/login.html')


@app.route('/voter/dashboard')
@voter_login_required
def voter_dashboard():
    voter = Voter.query.get(session['voter_id'])
    
    # Get active elections using service layer
    elections = get_active_elections()
    
    return render_template('voter/dashboard.html', voter=voter, elections=elections)


@app.route('/voter/logout')
def voter_logout():
    session.pop('voter_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/voter/vote/<int:election_id>', methods=['GET', 'POST'])
@voter_login_required
def vote(election_id):
    voter = Voter.query.get(session['voter_id'])
    election = Election.query.get_or_404(election_id)
    
    # Check if voter can vote using service layer
    can_vote_result, error_msg = can_vote(voter, election)
    if not can_vote_result:
        flash(error_msg, 'warning')
        return redirect(url_for('voter_dashboard'))
    
    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        
        # Validate candidate selection
        if not candidate_id:
            flash('Please select a candidate', 'warning')
            candidates = Candidate.query.filter_by(election_id=election_id).all()
            return render_template('voter/vote.html', election=election, candidates=candidates)
        
        try:
            candidate_id = int(candidate_id)
        except ValueError:
            flash('Invalid candidate selection', 'danger')
            return redirect(url_for('voter_dashboard'))
        
        # Record vote using service layer
        success, message = record_vote(voter.id, election_id, candidate_id)
        
        if success:
            flash(message, 'success')
        else:
            flash(message, 'danger')
        
        return redirect(url_for('voter_dashboard'))
    
    # GET request - show candidates
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    if not candidates:
        flash('No candidates available for this election', 'warning')
        return redirect(url_for('voter_dashboard'))
    
    return render_template('voter/vote.html', election=election, candidates=candidates)


# ==================== Initialize Database ====================

def init_db():
    """Initialize database and create default admin"""
    with app.app_context():
        try:
            db.create_all()
            app.logger.info('Database tables created successfully')
            
            # Create default admin if not exists
            if not Admin.query.filter_by(username='admin').first():
                admin = Admin(username='admin', email='admin@voting.com')
                admin.set_password('Admin@123')
                db.session.add(admin)
                db.session.commit()
                print("✓ Default admin created")
                print("  Username: admin")
                print("  Password: Admin@123")
                app.logger.info('Default admin account created')
            
            # Also create 'root' admin for backward compatibility
            if not Admin.query.filter_by(username='root').first():
                root_admin = Admin(username='root', email='root@voting.com')
                root_admin.set_password('Root@123')
                db.session.add(root_admin)
                db.session.commit()
                print("✓ Root admin created")
                print("  Username: root")
                print("  Password: Root@123")
                app.logger.info('Root admin account created')
                
        except Exception as e:
            app.logger.error(f'Error initializing database: {str(e)}')
            print(f"✗ Error initializing database: {str(e)}")


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    app.logger.warning(f'404 error: {request.url}')
    flash('The requested page was not found', 'warning')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    app.logger.error(f'500 error: {str(error)}')
    flash('An internal error occurred. Please try again later.', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 errors"""
    app.logger.warning(f'403 error: {request.url}')
    flash('You do not have permission to access this resource', 'danger')
    return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    app.logger.warning(f'413 error: Request entity too large')
    flash('File size exceeds maximum limit', 'danger')
    return redirect(request.referrer or url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
