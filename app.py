from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ==================== Models ====================

class College(db.Model):
    __tablename__ = 'colleges'
    id = db.Column(db.Integer, primary_key=True)
    college_code = db.Column(db.String(20), unique=True, nullable=False)
    college_name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    users = db.relationship('Admin', backref='college', lazy=True)
    elections = db.relationship('Election', backref='college', lazy=True)
    voters = db.relationship('Voter', backref='college', lazy=True)


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='admin')  # 'admin' or 'teacher'
    college_code = db.Column(db.String(20), db.ForeignKey('colleges.college_code'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_super_admin(self):
        return self.role == 'admin' and self.college_code is None
    
    def is_teacher(self):
        return self.role == 'teacher'


class Election(db.Model):
    __tablename__ = 'elections'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, active, completed
    college_code = db.Column(db.String(20), db.ForeignKey('colleges.college_code'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    candidates = db.relationship('Candidate', backref='election', lazy=True, cascade='all, delete-orphan')
    votes = db.relationship('Vote', backref='election', lazy=True, cascade='all, delete-orphan')
    creator = db.relationship('Admin', foreign_keys=[created_by])

    def update_status(self):
        now = datetime.now()
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
    voter_id = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    college_code = db.Column(db.String(20), db.ForeignKey('colleges.college_code'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
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
    timestamp = db.Column(db.DateTime, default=datetime.now)


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


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
        username = request.form.get('username')
        password = request.form.get('password')
        college_code = request.form.get('college_code', '').strip()
        
        # Super admin login (no college code)
        if not college_code:
            admin = Admin.query.filter_by(username=username, college_code=None).first()
        else:
            # Teacher login (with college code)
            admin = Admin.query.filter_by(username=username, college_code=college_code).first()
        
        if admin and admin.check_password(password):
            login_user(admin)
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials or college code', 'danger')
    
    return render_template('admin/login.html')


@app.route('/admin/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Super admin sees all elections
    if current_user.is_super_admin():
        elections = Election.query.all()
    else:
        # Teachers see only their college's elections
        elections = Election.query.filter_by(college_code=current_user.college_code).all()
    
    for election in elections:
        election.update_status()
    db.session.commit()
    
    if current_user.is_super_admin():
        total_elections = Election.query.count()
        total_candidates = Candidate.query.count()
        total_voters = Voter.query.count()
        total_votes = Vote.query.count()
    else:
        total_elections = Election.query.filter_by(college_code=current_user.college_code).count()
        total_candidates = db.session.query(Candidate).join(Election).filter(
            Election.college_code == current_user.college_code).count()
        total_voters = Voter.query.filter_by(college_code=current_user.college_code).count()
        total_votes = db.session.query(Vote).join(Election).filter(
            Election.college_code == current_user.college_code).count()
    
    return render_template('admin/dashboard.html', 
                         elections=elections,
                         total_elections=total_elections,
                         total_candidates=total_candidates,
                         total_voters=total_voters,
                         total_votes=total_votes)


@app.route('/admin/elections')
@login_required
def manage_elections():
    if current_user.is_super_admin():
        elections = Election.query.all()
        colleges = College.query.all()
    else:
        elections = Election.query.filter_by(college_code=current_user.college_code).all()
        colleges = []
    return render_template('admin/elections.html', elections=elections, colleges=colleges)


@app.route('/admin/elections/add', methods=['GET', 'POST'])
@login_required
def add_election():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%dT%H:%M')
        end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%dT%H:%M')
        
        # Super admin can select college, teachers use their own college
        if current_user.is_super_admin():
            college_code = request.form.get('college_code')
        else:
            college_code = current_user.college_code
        
        election = Election(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            college_code=college_code,
            created_by=current_user.id
        )
        election.update_status()
        
        db.session.add(election)
        db.session.commit()
        flash('Election created successfully!', 'success')
        return redirect(url_for('manage_elections'))
    
    # Get colleges for super admin
    colleges = College.query.all() if current_user.is_super_admin() else []
    return render_template('admin/add_election.html', colleges=colleges)


@app.route('/admin/elections/<int:election_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_election(election_id):
    election = Election.query.get_or_404(election_id)
    
    if request.method == 'POST':
        election.title = request.form.get('title')
        election.description = request.form.get('description')
        election.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%dT%H:%M')
        election.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%dT%H:%M')
        election.update_status()
        
        db.session.commit()
        flash('Election updated successfully!', 'success')
        return redirect(url_for('manage_elections'))
    
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
        name = request.form.get('name')
        party = request.form.get('party')
        description = request.form.get('description')
        photo_url = request.form.get('photo_url')
        
        candidate = Candidate(
            name=name,
            party=party,
            description=description,
            photo_url=photo_url,
            election_id=election_id
        )
        
        db.session.add(candidate)
        db.session.commit()
        flash('Candidate added successfully!', 'success')
        return redirect(url_for('manage_candidates', election_id=election_id))
    
    return render_template('admin/add_candidate.html', election=election)


@app.route('/admin/candidates/<int:candidate_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    
    if request.method == 'POST':
        candidate.name = request.form.get('name')
        candidate.party = request.form.get('party')
        candidate.description = request.form.get('description')
        candidate.photo_url = request.form.get('photo_url')
        
        db.session.commit()
        flash('Candidate updated successfully!', 'success')
        return redirect(url_for('manage_candidates', election_id=candidate.election_id))
    
    return render_template('admin/edit_candidate.html', candidate=candidate)


@app.route('/admin/candidates/<int:candidate_id>/delete', methods=['POST'])
@login_required
def delete_candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    election_id = candidate.election_id
    db.session.delete(candidate)
    db.session.commit()
    flash('Candidate deleted successfully!', 'success')
    return redirect(url_for('manage_candidates', election_id=election_id))


@app.route('/admin/elections/<int:election_id>/results')
@login_required
def view_results(election_id):
    election = Election.query.get_or_404(election_id)
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    results = []
    for candidate in candidates:
        results.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'votes': candidate.get_vote_count()
        })
    
    total_votes = sum(r['votes'] for r in results)
    
    # Get detailed vote information (who voted for whom) - for admin and teachers only
    detailed_votes = []
    votes = Vote.query.filter_by(election_id=election_id).all()
    for vote in votes:
        detailed_votes.append({
            'voter_name': vote.voter.name,
            'voter_id': vote.voter.voter_id,
            'candidate_name': vote.candidate.name,
            'timestamp': vote.timestamp
        })
    
    return render_template('admin/results.html', 
                         election=election, 
                         results=results,
                         total_votes=total_votes,
                         detailed_votes=detailed_votes)


@app.route('/api/elections/<int:election_id>/results')
def api_results(election_id):
    election = Election.query.get_or_404(election_id)
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    
    results = []
    for candidate in candidates:
        results.append({
            'id': candidate.id,
            'name': candidate.name,
            'party': candidate.party,
            'votes': candidate.get_vote_count()
        })
    
    return jsonify(results)


@app.route('/voter/register', methods=['GET', 'POST'])
def voter_register():
    if request.method == 'POST':
        voter_id = request.form.get('voter_id')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        college_code = request.form.get('college_code')
        
        # Check if college exists
        college = College.query.filter_by(college_code=college_code).first()
        if not college:
            flash('Invalid college code!', 'danger')
            return redirect(url_for('voter_register'))
        
        # Check if voter ID exists for this college
        if Voter.query.filter_by(voter_id=voter_id, college_code=college_code).first():
            flash('Voter ID already exists for this college!', 'danger')
            return redirect(url_for('voter_register'))
        
        voter = Voter(voter_id=voter_id, name=name, email=email, college_code=college_code)
        voter.set_password(password)
        
        db.session.add(voter)
        db.session.commit()
        flash('Registration successful! Please login to vote.', 'success')
        return redirect(url_for('voter_login'))
    
    return render_template('voter/register.html')


@app.route('/voter/login', methods=['GET', 'POST'])
def voter_login():
    if request.method == 'POST':
        voter_id = request.form.get('voter_id')
        password = request.form.get('password')
        college_code = request.form.get('college_code')
        
        voter = Voter.query.filter_by(voter_id=voter_id, college_code=college_code).first()
        
        if voter and voter.check_password(password):
            session['voter_id'] = voter.id
            flash('Login successful!', 'success')
            return redirect(url_for('voter_dashboard'))
        else:
            flash('Invalid voter ID, password, or college code', 'danger')
    
    return render_template('voter/login.html')


@app.route('/voter/dashboard')
def voter_dashboard():
    if 'voter_id' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('voter_login'))
    
    voter = Voter.query.get(session['voter_id'])
    # Show only active elections from voter's college
    elections = Election.query.filter_by(
        status='active', 
        college_code=voter.college_code
    ).all()
    
    return render_template('voter/dashboard.html', voter=voter, elections=elections)


@app.route('/voter/logout')
def voter_logout():
    session.pop('voter_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/voter/vote/<int:election_id>', methods=['GET', 'POST'])
def vote(election_id):
    if 'voter_id' not in session:
        flash('Please login first!', 'warning')
        return redirect(url_for('voter_login'))
    
    voter = Voter.query.get(session['voter_id'])
    election = Election.query.get_or_404(election_id)
    
    if election.status != 'active':
        flash('This election is not currently active!', 'warning')
        return redirect(url_for('voter_dashboard'))
    
    if voter.has_voted(election_id):
        flash('You have already voted in this election!', 'warning')
        return redirect(url_for('voter_dashboard'))
    
    if request.method == 'POST':
        candidate_id = request.form.get('candidate_id')
        
        vote = Vote(
            voter_id=voter.id,
            election_id=election_id,
            candidate_id=candidate_id
        )
        
        db.session.add(vote)
        db.session.commit()
        flash('Your vote has been recorded successfully!', 'success')
        return redirect(url_for('voter_dashboard'))
    
    candidates = Candidate.query.filter_by(election_id=election_id).all()
    return render_template('voter/vote.html', election=election, candidates=candidates)


# ==================== College & Teacher Management ====================

@app.route('/admin/colleges', methods=['GET'])
@login_required
def manage_colleges():
    if not current_user.is_super_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    colleges = College.query.all()
    return render_template('admin/colleges.html', colleges=colleges)


@app.route('/admin/colleges/add', methods=['POST'])
@login_required
def add_college():
    if not current_user.is_super_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    college_code = request.form.get('college_code').strip().upper()
    college_name = request.form.get('college_name')
    
    if College.query.filter_by(college_code=college_code).first():
        flash('College code already exists!', 'danger')
        return redirect(url_for('manage_colleges'))
    
    college = College(college_code=college_code, college_name=college_name)
    db.session.add(college)
    db.session.commit()
    flash(f'College {college_name} added successfully!', 'success')
    return redirect(url_for('manage_colleges'))


@app.route('/admin/teachers', methods=['GET'])
@login_required
def manage_teachers():
    if not current_user.is_super_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    teachers = Admin.query.filter_by(role='teacher').all()
    colleges = College.query.all()
    return render_template('admin/teachers.html', teachers=teachers, colleges=colleges)


@app.route('/admin/teachers/add', methods=['POST'])
@login_required
def add_teacher():
    if not current_user.is_super_admin():
        flash('Access denied!', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    college_code = request.form.get('college_code')
    
    # Check if college exists
    if not College.query.filter_by(college_code=college_code).first():
        flash('Invalid college code!', 'danger')
        return redirect(url_for('manage_teachers'))
    
    teacher = Admin(
        username=username,
        email=email,
        role='teacher',
        college_code=college_code
    )
    teacher.set_password(password)
    
    db.session.add(teacher)
    db.session.commit()
    flash(f'Teacher {username} added successfully!', 'success')
    return redirect(url_for('manage_teachers'))


# ==================== Database Viewer ====================

@app.route('/admin/database')
@login_required
def view_database():
    if not current_user.is_super_admin():
        flash('Access denied! Super admin only.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    # Get all data from tables
    colleges = College.query.all()
    admins = Admin.query.all()
    voters = Voter.query.all()
    elections = Election.query.all()
    candidates = Candidate.query.all()
    votes = Vote.query.all()
    
    return render_template('admin/database.html',
                         colleges=colleges,
                         admins=admins,
                         voters=voters,
                         elections=elections,
                         candidates=candidates,
                         votes=votes)


# ==================== Initialize Database ====================

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default super admin if not exists (no college code)
        if not Admin.query.filter_by(username='admin', college_code=None).first():
            admin = Admin(
                username='admin', 
                email='admin@voting.com',
                role='admin',
                college_code=None
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            # print("Default super admin created: username='admin', password='admin123' (no college code needed)")


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
