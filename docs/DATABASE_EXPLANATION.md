# Database Explanation - SQLAlchemy & MySQL

## 📋 Overview

This document explains the database design, relationships, and how SQLAlchemy ORM works in this project.

---

## 🗄️ Database Technology Stack

| Technology | Purpose | Why Used |
|------------|---------|----------|
| **MySQL** | Database management system | Reliable, widely used, free |
| **SQLAlchemy** | ORM (Object-Relational Mapping) | Write Python instead of SQL |
| **PyMySQL** | MySQL driver for Python | Connects Python to MySQL |

---

## 🏗️ Database Schema

### **Complete Entity-Relationship Diagram**

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│    ADMIN    │────────>│   ELECTION   │<────────│    VOTER    │
│             │ creates │              │  votes  │             │
│  id (PK)    │         │  id (PK)     │   in    │  id (PK)    │
│  username   │         │  title       │         │  voter_id   │
│  email      │         │  start_date  │         │  name       │
│  password   │         │  end_date    │         │  email      │
└─────────────┘         │  status      │         │  password   │
                        │  created_by  │         └─────────────┘
                        └──────────────┘
                               |
                               | contains
                               ↓
                        ┌──────────────┐
                        │  CANDIDATE   │
                        │              │
                        │  id (PK)     │
                        │  name        │
                        │  party       │
                        │  photo_url   │
                        │  election_id │
                        └──────────────┘
                               ↑
                               | receives
                               |
                        ┌──────────────┐
                        │     VOTE     │
                        │              │
                        │  id (PK)     │
                        │  voter_id    │
                        │  election_id │
                        │  candidate_id│
                        │  voted_at    │
                        └──────────────┘
```

---

## 📊 Table Structures in Detail

### **1. Admins Table**

```sql
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email)
);
```

**Field Explanations:**

| Field | Type | Purpose | Why This Type? |
|-------|------|---------|----------------|
| `id` | INT | Unique identifier | Auto-increment, fast lookups |
| `username` | VARCHAR(80) | Login name | Short, indexed for quick search |
| `email` | VARCHAR(120) | Contact & recovery | Standard email length |
| `password_hash` | VARCHAR(255) | Encrypted password | Bcrypt hash needs ~60 chars, buffer for algorithm changes |
| `created_at` | DATETIME | Registration time | Track account age, audit trail |

**Constraints:**
- `UNIQUE` on username: No duplicate usernames
- `UNIQUE` on email: One account per email
- `NOT NULL`: These fields are mandatory

**Indexes:**
- `idx_username`: Speeds up login queries
- `idx_email`: Speeds up email lookups

---

### **2. Voters Table**

```sql
CREATE TABLE voters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    voter_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_voter_id (voter_id),
    INDEX idx_email (email)
);
```

**Why separate from Admins?**
- Different permissions (voters can't create elections)
- Different data fields (voter_id vs username)
- Easier to manage security
- Better scalability

**voter_id vs id:**
- `id`: Internal database ID (auto-generated)
- `voter_id`: Public-facing ID (user chooses, like "VOTER123")
- WHY: Users remember "VOTER123" better than database ID "4732"

---

### **3. Elections Table**

```sql
CREATE TABLE elections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'upcoming',
    created_by INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (created_by) REFERENCES admins(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_dates (start_date, end_date)
);
```

**Status Values:**
- `upcoming`: Not started yet
- `active`: Currently open for voting
- `completed`: Finished

**Why TEXT for description?**
- Can store long descriptions (up to 65,535 characters)
- VARCHAR is limited to 255

**Foreign Key Explained:**

```sql
FOREIGN KEY (created_by) REFERENCES admins(id) ON DELETE SET NULL
```

**What this means:**
- `created_by` must match an `id` in `admins` table
- If admin is deleted, `created_by` becomes NULL (not deleted)
- `ON DELETE CASCADE` would delete election too
- `ON DELETE SET NULL` preserves election data

**Composite Index on Dates:**
```sql
INDEX idx_dates (start_date, end_date)
```
- Speeds up queries that filter by date range
- Used when finding active elections

---

### **4. Candidates Table**

```sql
CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    party VARCHAR(100),
    description TEXT,
    photo_url VARCHAR(255),
    election_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (election_id) REFERENCES elections(id) ON DELETE CASCADE,
    INDEX idx_election (election_id)
);
```

**Why ON DELETE CASCADE here?**

```sql
ON DELETE CASCADE
```

**Scenario:**
1. Admin deletes an election
2. CASCADE automatically deletes all candidates in that election
3. Prevents orphaned candidates (candidates without election)

**Without CASCADE:**
```
Election deleted → Candidates still exist → Database inconsistency
```

**With CASCADE:**
```
Election deleted → Candidates automatically deleted → Clean database
```

**photo_url field:**
- Stores URL to candidate photo
- Can be external (imgur.com/photo.jpg) or local (/static/photos/candidate1.jpg)
- NULL allowed (some candidates might not have photos)

---

### **5. Votes Table (Most Complex)**

```sql
CREATE TABLE votes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    voter_id INT NOT NULL,
    election_id INT NOT NULL,
    candidate_id INT NOT NULL,
    voted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (voter_id) REFERENCES voters(id) ON DELETE CASCADE,
    FOREIGN KEY (election_id) REFERENCES elections(id) ON DELETE CASCADE,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_vote (voter_id, election_id),
    INDEX idx_election_candidate (election_id, candidate_id)
);
```

**Critical Constraint:**

```sql
UNIQUE KEY unique_vote (voter_id, election_id)
```

**What this does:**
- Prevents same voter from voting twice in same election
- Database-level enforcement (can't be bypassed)
- Combination of (voter_id, election_id) must be unique

**Examples:**

✅ **Allowed:**
```
voter_id=1, election_id=1, candidate_id=5
voter_id=1, election_id=2, candidate_id=3  ← Different election
voter_id=2, election_id=1, candidate_id=5  ← Different voter
```

❌ **Blocked:**
```
voter_id=1, election_id=1, candidate_id=5
voter_id=1, election_id=1, candidate_id=7  ← Same voter + election!
```

**Why three foreign keys?**
1. `voter_id` → Who voted (links to voters table)
2. `election_id` → Which election (links to elections table)
3. `candidate_id` → For whom (links to candidates table)

**Composite Index:**

```sql
INDEX idx_election_candidate (election_id, candidate_id)
```

- Speeds up result counting
- Query: "How many votes did candidate X get in election Y?"
- Optimized for this specific lookup pattern

---

## 🔗 Relationships Explained

### **One-to-Many Relationship**

#### **Admin → Elections**

```python
# In Admin model
elections = db.relationship('Election', backref='creator', lazy=True)

# In Election model
created_by = db.Column(db.Integer, db.ForeignKey('admins.id'))
```

**What you can do:**

```python
# Get all elections by an admin
admin = Admin.query.get(1)
my_elections = admin.elections  # List of Election objects

# Get creator of an election
election = Election.query.get(5)
creator = election.creator  # Admin object
```

**Real-world analogy:**
- One author (Admin) writes many books (Elections)
- Each book has exactly one author

---

#### **Election → Candidates**

```python
# In Election model
candidates = db.relationship('Candidate', backref='election', 
                            lazy=True, cascade='all, delete-orphan')

# In Candidate model
election_id = db.Column(db.Integer, db.ForeignKey('elections.id'))
```

**Usage:**

```python
# Get all candidates in an election
election = Election.query.get(3)
all_candidates = election.candidates

# Get election of a candidate
candidate = Candidate.query.get(10)
his_election = candidate.election
```

---

### **Many-to-Many Relationship (via Vote)**

#### **Voters ↔ Candidates (through Votes)**

```
Voter ──→ Vote ──→ Candidate
         ↓
      Election
```

**Why not direct relationship?**

❌ **Without Vote table:**
```
voters_candidates table:
voter_id | candidate_id
```
Problem: Can't track WHEN they voted or WHICH election

✅ **With Vote table:**
```
votes table:
voter_id | election_id | candidate_id | voted_at
```
Benefits:
- Know when vote was cast
- Know which election it was for
- Can have same voter vote in multiple elections
- Can generate reports and analytics

---

## 🔍 SQLAlchemy Query Examples

### **Basic Queries**

```python
# Get all admins
admins = Admin.query.all()

# Get one admin by ID
admin = Admin.query.get(5)

# Get admin by username
admin = Admin.query.filter_by(username='john').first()

# Get multiple with filter
active_elections = Election.query.filter_by(status='active').all()
```

---

### **Complex Queries**

#### **Get elections created by specific admin**

```python
admin_id = 3
elections = Election.query.filter_by(created_by=admin_id).all()

# OR using relationship
admin = Admin.query.get(3)
elections = admin.elections
```

---

#### **Count votes for a candidate**

```python
candidate_id = 10
election_id = 5

vote_count = Vote.query.filter_by(
    candidate_id=candidate_id,
    election_id=election_id
).count()
```

**SQL equivalent:**
```sql
SELECT COUNT(*) FROM votes 
WHERE candidate_id = 10 AND election_id = 5;
```

---

#### **Check if voter already voted**

```python
voter_id = 7
election_id = 2

existing_vote = Vote.query.filter_by(
    voter_id=voter_id,
    election_id=election_id
).first()

if existing_vote:
    print("Already voted!")
else:
    print("Can vote")
```

---

#### **Get election results**

```python
from sqlalchemy import func

election_id = 3

# Get vote counts per candidate
results = db.session.query(
    Candidate.name,
    func.count(Vote.id).label('vote_count')
).join(
    Vote, Vote.candidate_id == Candidate.id
).filter(
    Vote.election_id == election_id
).group_by(
    Candidate.id
).all()

# Result: [('John Doe', 150), ('Jane Smith', 200), ...]
```

**SQL equivalent:**
```sql
SELECT candidates.name, COUNT(votes.id) as vote_count
FROM candidates
JOIN votes ON votes.candidate_id = candidates.id
WHERE votes.election_id = 3
GROUP BY candidates.id;
```

---

#### **Get active elections (date range)**

```python
from datetime import datetime

now = datetime.utcnow()

active = Election.query.filter(
    Election.start_date <= now,
    Election.end_date >= now
).all()
```

**Breakdown:**
- `start_date <= now`: Election has started
- `end_date >= now`: Election hasn't ended
- Both conditions: Currently active

---

### **Aggregation Queries**

```python
# Total votes in an election
total_votes = Vote.query.filter_by(election_id=5).count()

# Total elections
total_elections = Election.query.count()

# Elections by admin
admin_election_count = Election.query.filter_by(created_by=3).count()

# Voters who voted
voters_voted = db.session.query(Vote.voter_id).distinct().count()
```

---

## 🔒 Database Security Features

### **1. Password Hashing**

```python
# Never store plain passwords!
password = "secret123"

# ❌ BAD
admin.password = password

# ✅ GOOD
admin.password_hash = generate_password_hash(password)
```

**How it works:**
```
Input: "admin123"
↓
Salt: Random data added
↓
Hash Function: SHA-256 + Bcrypt
↓
Output: "$2b$12$xyz...abc" (60 characters)
```

**Why secure?**
- One-way function (can't reverse)
- Same password = different hashes (due to salt)
- Slow algorithm (prevents brute force)

---

### **2. SQL Injection Prevention**

❌ **Vulnerable Code:**
```python
username = request.form.get('username')
query = f"SELECT * FROM admins WHERE username = '{username}'"
db.execute(query)
```

**Attack:**
```
username = "admin' OR '1'='1"
Query becomes: SELECT * FROM admins WHERE username = 'admin' OR '1'='1'
Result: Returns all admins!
```

✅ **Safe Code (SQLAlchemy):**
```python
username = request.form.get('username')
admin = Admin.query.filter_by(username=username).first()
```

**Why safe:**
- SQLAlchemy uses parameterized queries
- Input is treated as data, not SQL code
- Special characters are escaped

---

### **3. Foreign Key Constraints**

```python
# Try to create vote for non-existent candidate
vote = Vote(voter_id=1, election_id=1, candidate_id=9999)
db.session.add(vote)
db.session.commit()
# ❌ Error! candidate_id=9999 doesn't exist
```

**Benefits:**
- Can't reference non-existent records
- Maintains data integrity
- Prevents orphaned records

---

## 📈 Database Performance Tips

### **1. Indexes**

```python
# Add index to frequently queried column
class Election(db.Model):
    status = db.Column(db.String(20), index=True)
```

**When to index:**
- Fields used in WHERE clauses
- Foreign keys
- Fields used for sorting
- UNIQUE fields

**When NOT to index:**
- Small tables
- Fields that change frequently
- Fields with few distinct values

---

### **2. Lazy Loading vs Eager Loading**

```python
# Lazy Loading (default)
elections = Election.query.all()
for election in elections:
    print(election.candidates)  # Separate query for each!
# Problem: N+1 queries (1 for elections + N for candidates)

# Eager Loading (better)
from sqlalchemy.orm import joinedload

elections = Election.query.options(
    joinedload(Election.candidates)
).all()
for election in elections:
    print(election.candidates)  # Already loaded!
# Result: 1 query with JOIN
```

---

### **3. Pagination**

```python
# Without pagination - loads all records
elections = Election.query.all()  # Could be 10,000 records!

# With pagination - loads only what's needed
page = 1
per_page = 20

elections = Election.query.paginate(
    page=page, 
    per_page=per_page, 
    error_out=False
)

# Access results
items = elections.items
total = elections.total
has_next = elections.has_next
```

---

## 🛠️ Database Maintenance

### **Creating Tables**

```python
# In app.py
with app.app_context():
    db.create_all()
    print("Tables created!")
```

**What happens:**
- Reads all model definitions
- Creates corresponding SQL tables
- Adds indexes and constraints

---

### **Backup and Restore**

```bash
# Backup
mysqldump -u root -p voting_system > backup.sql

# Restore
mysql -u root -p voting_system < backup.sql
```

---

### **Reset Database**

```python
# WARNING: Deletes all data!
with app.app_context():
    db.drop_all()  # Delete all tables
    db.create_all()  # Recreate them
```

---

## 📊 Sample Data Workflow

```python
# 1. Create Admin
admin = Admin(username='admin', email='admin@vote.com')
admin.set_password('Admin@123')
db.session.add(admin)
db.session.commit()

# 2. Create Election
election = Election(
    title='Class President 2025',
    description='Vote for your president',
    start_date=datetime(2025, 1, 1, 9, 0),
    end_date=datetime(2025, 1, 7, 17, 0),
    created_by=admin.id
)
db.session.add(election)
db.session.commit()

# 3. Add Candidates
candidate1 = Candidate(
    name='John Doe',
    party='Student Party',
    election_id=election.id
)
candidate2 = Candidate(
    name='Jane Smith',
    party='Progressive Party',
    election_id=election.id
)
db.session.add_all([candidate1, candidate2])
db.session.commit()

# 4. Create Voter
voter = Voter(
    voter_id='VOTER001',
    name='Mike Johnson',
    email='mike@student.com'
)
voter.set_password('password123')
db.session.add(voter)
db.session.commit()

# 5. Cast Vote
vote = Vote(
    voter_id=voter.id,
    election_id=election.id,
    candidate_id=candidate1.id
)
db.session.add(vote)
db.session.commit()

print("Complete voting workflow created!")
```

---

## 🎓 Key Takeaways

1. **Foreign Keys** maintain relationships and data integrity
2. **Indexes** speed up queries but take storage space
3. **Unique Constraints** prevent duplicate data
4. **Cascade Options** control what happens when parent is deleted
5. **SQLAlchemy** translates Python code to SQL automatically
6. **Relationships** make code cleaner and more Pythonic

---

**Next:** Read [Frontend Explanation](FRONTEND_EXPLANATION.md) to learn about templates!
