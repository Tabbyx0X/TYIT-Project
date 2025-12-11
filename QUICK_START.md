# Quick Start Guide - Online Voting System

## Prerequisites Checklist
- [ ] Python 3.8+ installed
- [ ] MySQL Server 8.0+ installed and running
- [ ] Git (optional)

## Installation Steps

### Option 1: Automated Setup (Recommended)

1. **Open PowerShell in project directory**
   ```powershell
   cd "d:\College Assignments\TYIT\Project-Code"
   ```

2. **Run setup script**
   ```powershell
   .\setup.ps1
   ```
   
   If you get an error, enable script execution:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Edit .env file** with your MySQL credentials
   - Open `.env` in any text editor
   - Update `DATABASE_PASSWORD` with your MySQL password

4. **Run the application**
   ```powershell
   .\run.ps1
   ```

### Option 2: Manual Setup

1. **Create virtual environment**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Create database**
   ```sql
   CREATE DATABASE voting_system;
   ```

4. **Configure environment**
   ```powershell
   Copy-Item .env.example .env
   ```
   Edit `.env` with your credentials

5. **Run application**
   ```powershell
   python app.py
   ```

## First Time Access

### Admin Access
1. Open browser: `http://localhost:5000`
2. Click "Admin Login"
3. Login with:
   - Username: `admin`
   - Password: `admin123`

### Create Your First Election

1. From Admin Dashboard, click "Create Election"
2. Fill in:
   - Title: e.g., "Student Council Election 2024"
   - Description
   - Start Date & Time
   - End Date & Time
3. Click "Create Election"

### Add Candidates

1. Click "Manage Candidates" for your election
2. Click "Add Candidate"
3. Fill in candidate details:
   - Name
   - Party (optional)
   - Description (optional)
   - Photo URL (optional)
4. Add at least 2 candidates

### Test Voting

1. Open a new browser window (or incognito mode)
2. Click "Voter Register"
3. Create a voter account:
   - Voter ID: any unique ID (e.g., "V001")
   - Name
   - Email
   - Password
4. Login with voter credentials
5. Click "Cast Your Vote"
6. Select a candidate
7. Submit vote

### View Results

1. Return to Admin panel
2. Click "View Results" for the election
3. See real-time charts and vote counts

## Common Issues & Solutions

### MySQL Connection Error
**Problem:** Cannot connect to database
**Solution:**
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists: `CREATE DATABASE voting_system;`

### Port Already in Use
**Problem:** Port 5000 is busy
**Solution:**
- Edit `app.py`, change: `app.run(port=5001)`

### Virtual Environment Issues
**Problem:** venv activation fails
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Module Not Found
**Problem:** Import errors
**Solution:**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Project URLs

| Page | URL | Access |
|------|-----|--------|
| Home | http://localhost:5000 | Public |
| Admin Login | http://localhost:5000/admin/login | Admin |
| Admin Dashboard | http://localhost:5000/admin/dashboard | Admin |
| Voter Register | http://localhost:5000/voter/register | Public |
| Voter Login | http://localhost:5000/voter/login | Public |
| Voter Dashboard | http://localhost:5000/voter/dashboard | Voter |

## Default Credentials

### Admin
- **Username:** admin
- **Password:** admin123

**⚠️ Change password after first login!**

## Features Overview

### Admin Features
✅ Create and manage elections
✅ Add and manage candidates  
✅ View real-time results
✅ Bar and pie charts
✅ Election status tracking
✅ Dashboard with statistics

### Voter Features
✅ Secure registration
✅ Login system
✅ View active elections
✅ Cast votes
✅ Vote confirmation
✅ One vote per election

## Tips for Demonstration

1. **Prepare Sample Data:**
   - Create 2-3 elections with different statuses
   - Add 3-4 candidates per election
   - Register 5-10 test voters
   - Cast some sample votes

2. **Show Real-time Updates:**
   - Open results page in one window
   - Cast votes in another window
   - Charts will update automatically

3. **Highlight Security:**
   - Demonstrate one-vote-per-election
   - Show password hashing
   - Explain session management

4. **Show Responsive Design:**
   - Open on mobile/tablet view
   - Demonstrate Bootstrap responsiveness

## Next Steps

After basic setup:
1. Change admin password
2. Add real election data
3. Test all features
4. Customize styling (optional)
5. Add sample voters for demo

## Support

For issues:
1. Check this guide
2. Review README.md
3. Check error messages in console
4. Verify MySQL connection

## Quick Commands Reference

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run application
python app.py

# Install new packages
pip install package-name
pip freeze > requirements.txt

# MySQL commands
mysql -u root -p
CREATE DATABASE voting_system;
USE voting_system;
SHOW TABLES;
```

---

**Happy Voting! 🗳️**
