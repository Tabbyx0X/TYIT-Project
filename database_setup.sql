# Database Setup SQL Script

-- Create database
CREATE DATABASE IF NOT EXISTS voting_system;
USE voting_system;

-- The tables will be automatically created by SQLAlchemy when you run app.py
-- However, if you want to create them manually, here's the schema:

-- Admins table
CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Elections table
CREATE TABLE IF NOT EXISTS elections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'upcoming',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Candidates table
CREATE TABLE IF NOT EXISTS candidates (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    party VARCHAR(100),
    description TEXT,
    photo_url VARCHAR(255),
    election_id INT NOT NULL,
    FOREIGN KEY (election_id) REFERENCES elections(id) ON DELETE CASCADE
);

-- Voters table
CREATE TABLE IF NOT EXISTS voters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    voter_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Votes table
CREATE TABLE IF NOT EXISTS votes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    voter_id INT NOT NULL,
    election_id INT NOT NULL,
    candidate_id INT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (voter_id) REFERENCES voters(id) ON DELETE CASCADE,
    FOREIGN KEY (election_id) REFERENCES elections(id) ON DELETE CASCADE,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    UNIQUE KEY unique_vote (voter_id, election_id)
);

-- Create default admin (password: admin123)
-- Note: The password hash is for 'root'
INSERT INTO admins (username, password_hash, email)
VALUES ('admin', 'pbkdf2:sha256:600000$salt$hash', 'admin@voting.com')
ON DUPLICATE KEY UPDATE username=username;

-- Sample data (optional)

-- Insert sample election
INSERT INTO elections (title, description, start_date, end_date, status)
VALUES 
('Student Council Election 2024', 'Annual student council election', 
 '2024-10-01 09:00:00', '2024-12-31 17:00:00', 'active');

-- Insert sample candidates (adjust election_id as needed)
INSERT INTO candidates (name, party, description, election_id)
VALUES 
('John Doe', 'Independent', 'Experienced leader with vision for change', 1),
('Jane Smith', 'Student Party', 'Committed to student welfare', 1),
('Mike Johnson', 'Progressive Alliance', 'Innovation and technology advocate', 1);
