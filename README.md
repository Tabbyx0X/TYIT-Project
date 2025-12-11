# Online Voting System

A secure, web-based voting platform built with Flask (Python) backend, MySQL database, and modern Bootstrap frontend.

## Features

### Admin Panel
- ✅ Admin authentication and login
- ✅ Create, edit, and delete elections
- ✅ Add, edit, and delete candidates
- ✅ Real-time vote results viewing
- ✅ Interactive charts (Bar & Pie) using Chart.js
- ✅ Dashboard with statistics

### Voter Features
- ✅ Voter registration and login
- ✅ View active elections
- ✅ Cast votes (one vote per election)
- ✅ Secure vote storage
- ✅ Vote confirmation

### Security Features
- Password hashing using Werkzeug
- Session-based authentication
- One vote per voter per election
- Vote integrity checks

## Technology Stack

- **Backend:** Python Flask
- **Database:** MySQL with SQLAlchemy ORM
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Charts:** Chart.js
- **Icons:** Font Awesome 6

## Prerequisites

- Python 3.8 or higher
- MySQL Server 8.0 or higher
- pip (Python package manager)

## Installation & Setup

### 1. Clone or Download the Project

```powershell
cd "d:\College Assignments\TYIT\Project-Code"
```

### 2. Create Virtual Environment (Recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Setup MySQL Database

1. Open MySQL Command Line or MySQL Workbench
2. Create a database:

```sql
CREATE DATABASE voting_system;
```

3. Create a MySQL user (optional but recommended):

```sql
CREATE USER 'voting_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON voting_system.* TO 'voting_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configure Environment Variables

1. Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

2. Edit `.env` file with your database credentials:

```env
SECRET_KEY=your-secret-key-here
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=your-mysql-password
DATABASE_NAME=voting_system
FLASK_ENV=development
```

### 6. Initialize Database

The application will automatically create all necessary tables on first run.

```powershell
python app.py
```

## Running the Application

```powershell
python app.py
```

The application will be available at: `http://localhost:5000`

## Default Credentials

### Admin Login
- **URL:** `http://localhost:5000/admin/login`
- **Username:** `admin`
- **Password:** `admin123`

**⚠️ Important:** Change the default admin password after first login!

## Database Schema

### Tables

1. **admins** - Admin user accounts
   - id, username, password_hash, email, created_at

2. **elections** - Election information
   - id, title, description, start_date, end_date, status, created_at

3. **candidates** - Election candidates
   - id, name, party, description, photo_url, election_id

4. **voters** - Registered voters
   - id, voter_id, name, email, password_hash, created_at

5. **votes** - Cast votes
   - id, voter_id, election_id, candidate_id, timestamp

## Usage Guide

### For Administrators

1. **Login:** Navigate to `/admin/login` and use admin credentials
2. **Create Election:**
   - Click "Create Election" from dashboard
   - Fill in election details (title, description, dates)
   - Submit the form
3. **Add Candidates:**
   - Go to "Manage Candidates" for an election
   - Click "Add Candidate"
   - Fill in candidate information
   - Optional: Add photo URL
4. **View Results:**
   - Click "View Results" for any election
   - See real-time bar and pie charts
   - Charts auto-refresh every 10 seconds for active elections

### For Voters

1. **Register:**
   - Go to "Voter Register"
   - Fill in voter ID, name, email, and password
   - Submit registration
2. **Login:**
   - Use voter ID and password to login
3. **Cast Vote:**
   - View active elections on dashboard
   - Click "Cast Your Vote"
   - Select a candidate
   - Confirm and submit

## API Endpoints

### Admin Routes
- `GET /admin/login` - Admin login page
- `POST /admin/login` - Process admin login
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/elections` - Manage elections
- `POST /admin/elections/add` - Create new election
- `POST /admin/elections/<id>/edit` - Edit election
- `POST /admin/elections/<id>/delete` - Delete election
- `GET /admin/elections/<id>/candidates` - Manage candidates
- `POST /admin/elections/<id>/candidates/add` - Add candidate
- `GET /admin/elections/<id>/results` - View results

### Voter Routes
- `GET /voter/register` - Voter registration page
- `POST /voter/register` - Process registration
- `GET /voter/login` - Voter login page
- `POST /voter/login` - Process voter login
- `GET /voter/dashboard` - Voter dashboard
- `GET /voter/vote/<election_id>` - Vote page
- `POST /voter/vote/<election_id>` - Submit vote

### API Routes
- `GET /api/elections/<id>/results` - Get election results as JSON

## Project Structure

```
Project-Code/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
├── .env.example               # Example environment file
├── .gitignore                 # Git ignore file
│
└── templates/                  # HTML templates
    ├── base.html              # Base template
    ├── index.html             # Home page
    │
    ├── admin/                 # Admin templates
    │   ├── login.html
    │   ├── dashboard.html
    │   ├── elections.html
    │   ├── add_election.html
    │   ├── edit_election.html
    │   ├── candidates.html
    │   ├── add_candidate.html
    │   ├── edit_candidate.html
    │   └── results.html
    │
    └── voter/                 # Voter templates
        ├── register.html
        ├── login.html
        ├── dashboard.html
        └── vote.html
```

## Features Demonstration

### Charts & Visualization
- **Bar Chart:** Shows vote counts for each candidate
- **Pie Chart:** Displays vote distribution percentage
- **Real-time Updates:** Auto-refresh for active elections
- **Responsive Design:** Works on all screen sizes

### Security Features
- Password hashing using Werkzeug
- CSRF protection with Flask-WTF
- Session management
- One vote per election enforcement
- SQL injection prevention via SQLAlchemy ORM

## Troubleshooting

### Common Issues

1. **MySQL Connection Error:**
   - Verify MySQL is running
   - Check database credentials in `.env`
   - Ensure database exists

2. **Module Not Found:**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Port Already in Use:**
   - Change port in `app.py`: `app.run(port=5001)`

4. **Database Tables Not Created:**
   - Delete database and restart application
   - Check MySQL user permissions

## Future Enhancements

- Email verification for voters
- Two-factor authentication
- Export results to PDF/CSV
- Advanced analytics dashboard
- Multi-language support
- Mobile app integration (Android)
- Blockchain-based voting for enhanced security

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is for educational purposes.

## Contact

For questions or support, please contact the development team.

---

**Note:** This is a college project and should not be used in production without proper security audits and enhancements.
