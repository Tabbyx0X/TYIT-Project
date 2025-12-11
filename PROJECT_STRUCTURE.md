# Project Structure Documentation

## Directory Structure

```
Project-Code/
│
├── app.py                          # Main Flask application file
│   ├── Models (Database tables)
│   ├── Routes (URL endpoints)
│   └── Database initialization
│
├── config.py                       # Configuration settings
│   └── Database connection settings
│
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
├── .env.example                   # Template for .env file
├── .gitignore                     # Git ignore rules
│
├── setup.ps1                      # Automated setup script (Windows)
├── run.ps1                        # Quick run script (Windows)
│
├── README.md                      # Comprehensive documentation
├── QUICK_START.md                 # Quick start guide
├── PROJECT_STRUCTURE.md           # This file
├── database_setup.sql             # SQL schema reference
│
├── static/                        # Static files (CSS, JS, images)
│   ├── css/
│   │   └── custom.css            # Custom styles
│   ├── js/
│   │   └── (if needed)
│   └── images/
│       └── (candidate photos, etc.)
│
└── templates/                     # HTML templates (Jinja2)
    ├── base.html                 # Base template (layout)
    ├── index.html                # Home page
    │
    ├── admin/                    # Admin panel templates
    │   ├── login.html           # Admin login page
    │   ├── dashboard.html       # Admin dashboard
    │   ├── elections.html       # Manage elections list
    │   ├── add_election.html    # Create election form
    │   ├── edit_election.html   # Edit election form
    │   ├── candidates.html      # Manage candidates list
    │   ├── add_candidate.html   # Add candidate form
    │   ├── edit_candidate.html  # Edit candidate form
    │   └── results.html         # Results with charts
    │
    └── voter/                   # Voter interface templates
        ├── register.html        # Voter registration
        ├── login.html          # Voter login
        ├── dashboard.html      # Voter dashboard
        └── vote.html           # Voting page
```

## File Descriptions

### Core Application Files

#### `app.py`
**Purpose:** Main application file
**Contains:**
- Flask app initialization
- Database models (Admin, Election, Candidate, Voter, Vote)
- All route handlers
- Database initialization function

**Key Models:**
```python
Admin       # Admin users
Election    # Election information
Candidate   # Election candidates
Voter       # Registered voters
Vote        # Cast votes
```

**Key Routes:**
```python
# Public
/                           # Home page
/voter/register            # Voter registration
/voter/login               # Voter login

# Admin (requires login)
/admin/login               # Admin login
/admin/dashboard           # Admin dashboard
/admin/elections           # Manage elections
/admin/elections/<id>/candidates  # Manage candidates
/admin/elections/<id>/results     # View results

# Voter (requires login)
/voter/dashboard           # Voter dashboard
/voter/vote/<election_id>  # Cast vote

# API
/api/elections/<id>/results  # JSON results
```

#### `config.py`
**Purpose:** Configuration management
**Contains:**
- Database connection settings
- Secret key configuration
- Environment variable loading

#### `requirements.txt`
**Purpose:** Python package dependencies
**Key Packages:**
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Flask-Login: User session management
- PyMySQL: MySQL database driver
- Werkzeug: Password hashing
- python-dotenv: Environment variables

### Template Files

#### `templates/base.html`
**Purpose:** Base template for all pages
**Contains:**
- HTML structure
- Bootstrap CSS
- Font Awesome icons
- Chart.js library
- Navigation bar
- Flash messages
- Footer

**Usage:** All other templates extend this

#### Admin Templates

1. **`admin/login.html`**
   - Admin authentication form
   - Username and password fields

2. **`admin/dashboard.html`**
   - Statistics cards
   - Elections table
   - Quick actions

3. **`admin/elections.html`**
   - List all elections
   - Edit/Delete actions

4. **`admin/add_election.html`**
   - Create election form
   - Date/time pickers

5. **`admin/edit_election.html`**
   - Update election details
   - Pre-filled form

6. **`admin/candidates.html`**
   - Grid of candidate cards
   - Add/Edit/Delete options

7. **`admin/add_candidate.html`**
   - Add candidate form
   - Photo URL field

8. **`admin/edit_candidate.html`**
   - Update candidate details

9. **`admin/results.html`**
   - Election information
   - Bar chart (Chart.js)
   - Pie chart (Chart.js)
   - Detailed results table
   - Real-time updates

#### Voter Templates

1. **`voter/register.html`**
   - Registration form
   - Voter ID, name, email, password

2. **`voter/login.html`**
   - Login form
   - Voter ID and password

3. **`voter/dashboard.html`**
   - Active elections list
   - Vote status indicators
   - Statistics

4. **`voter/vote.html`**
   - Candidate cards
   - Radio selection
   - Vote submission

### Configuration Files

#### `.env` (You need to create this)
**Purpose:** Environment variables
**Contains:**
```env
SECRET_KEY=your-secret-key
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=your-password
DATABASE_NAME=voting_system
```

#### `.env.example`
**Purpose:** Template for .env file
**Usage:** Copy to .env and fill in values

#### `.gitignore`
**Purpose:** Files to exclude from Git
**Excludes:**
- `.env` (sensitive data)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)

### Database Schema

#### Tables:

1. **admins**
   - id (PRIMARY KEY)
   - username (UNIQUE)
   - password_hash
   - email (UNIQUE)
   - created_at

2. **elections**
   - id (PRIMARY KEY)
   - title
   - description
   - start_date
   - end_date
   - status (upcoming/active/completed)
   - created_at

3. **candidates**
   - id (PRIMARY KEY)
   - name
   - party
   - description
   - photo_url
   - election_id (FOREIGN KEY → elections)

4. **voters**
   - id (PRIMARY KEY)
   - voter_id (UNIQUE)
   - name
   - email (UNIQUE)
   - password_hash
   - created_at

5. **votes**
   - id (PRIMARY KEY)
   - voter_id (FOREIGN KEY → voters)
   - election_id (FOREIGN KEY → elections)
   - candidate_id (FOREIGN KEY → candidates)
   - timestamp
   - UNIQUE(voter_id, election_id) # One vote per election

## Key Features Implementation

### Authentication
- **Admin:** Flask-Login with session management
- **Voter:** Custom session-based authentication
- **Password:** Werkzeug password hashing (pbkdf2:sha256)

### Security
- CSRF protection (Flask-WTF)
- Password hashing
- SQL injection prevention (SQLAlchemy ORM)
- Session management
- One vote per election constraint

### Real-time Updates
- AJAX polling every 10 seconds
- Chart.js dynamic updates
- JSON API endpoint

### Charts (Chart.js)
- Bar chart: Vote counts
- Pie chart: Vote distribution
- Responsive design
- Auto-refresh for active elections

### Responsive Design
- Bootstrap 5 framework
- Mobile-friendly
- Tablet optimized
- Desktop enhanced

## Data Flow

### Voting Process:
```
1. Voter registers → voters table
2. Voter logs in → session created
3. Voter views elections → query elections table
4. Voter selects candidate → vote.html
5. Vote submitted → votes table
6. Results updated → real-time charts
```

### Admin Process:
```
1. Admin logs in → admins table
2. Create election → elections table
3. Add candidates → candidates table
4. View results → JOIN votes + candidates
5. Charts rendered → Chart.js
```

## Extension Points

### Adding New Features:
1. **Email Notifications:** Add Flask-Mail
2. **File Uploads:** Add Flask-Uploads for photos
3. **API:** Expand REST API endpoints
4. **Android App:** Use Flask API backend
5. **Analytics:** Add more dashboard metrics

### Customization:
1. **Styling:** Edit `static/css/custom.css`
2. **Templates:** Modify HTML in `templates/`
3. **Routes:** Add to `app.py`
4. **Database:** Add models in `app.py`

## Development Workflow

### Adding a New Feature:

1. **Model:** Add/modify database model in `app.py`
2. **Route:** Add route handler in `app.py`
3. **Template:** Create/modify HTML template
4. **Test:** Run app and test feature
5. **Commit:** Save changes to Git

### Testing:
```powershell
# Run application
python app.py

# Test in browser
http://localhost:5000

# Check errors
# View Flask console output
```

## Deployment Considerations

For production:
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn)
3. Enable HTTPS
4. Configure proper MySQL user permissions
5. Set strong SECRET_KEY
6. Regular database backups
7. Monitor logs

## Troubleshooting

### Common Files to Check:
1. `.env` - Database credentials
2. `app.py` - Error messages in console
3. MySQL logs - Database connection issues
4. Browser console - JavaScript errors

## Documentation

- **README.md:** Complete project documentation
- **QUICK_START.md:** Fast setup guide
- **This File:** Structure reference
- **Code Comments:** In-line documentation

---

**For detailed instructions, see README.md and QUICK_START.md**
