# Online Voting System - Setup Script for Windows
# Run this script in PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Online Voting System - Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "  Download from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit
}

# Check if MySQL is installed
Write-Host "Checking MySQL installation..." -ForegroundColor Yellow
try {
    $mysqlVersion = mysql --version 2>&1
    Write-Host "✓ MySQL found: $mysqlVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ MySQL not found! Please install MySQL Server." -ForegroundColor Red
    Write-Host "  Download from: https://dev.mysql.com/downloads/mysql/" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 1: Creating Virtual Environment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (Test-Path "venv") {
    Write-Host "Virtual environment already exists." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created." -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 2: Activating Virtual Environment" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated." -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 3: Installing Dependencies" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

pip install --upgrade pip
pip install -r requirements.txt
Write-Host "✓ Dependencies installed." -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 4: Environment Configuration" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (Test-Path ".env") {
    Write-Host ".env file already exists." -ForegroundColor Yellow
} else {
    Copy-Item .env.example .env
    Write-Host "✓ .env file created from template." -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Edit .env file with your MySQL credentials!" -ForegroundColor Yellow
    Write-Host "  - DATABASE_USER=your_mysql_username" -ForegroundColor Yellow
    Write-Host "  - DATABASE_PASSWORD=your_mysql_password" -ForegroundColor Yellow
    Write-Host "  - DATABASE_NAME=voting_system" -ForegroundColor Yellow
    Write-Host ""
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Step 5: Database Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Please ensure you have:" -ForegroundColor Yellow
Write-Host "  1. MySQL server is running" -ForegroundColor Yellow
Write-Host "  2. Created database 'voting_system'" -ForegroundColor Yellow
Write-Host "  3. Updated .env file with correct credentials" -ForegroundColor Yellow
Write-Host ""

$createDb = Read-Host "Do you want to create the database now? (y/n)"
if ($createDb -eq "y") {
    $mysqlUser = Read-Host "Enter MySQL root username (default: root)"
    if ([string]::IsNullOrWhiteSpace($mysqlUser)) {
        $mysqlUser = "root"
    }
    
    Write-Host "Creating database..." -ForegroundColor Yellow
    $createDbQuery = "CREATE DATABASE IF NOT EXISTS voting_system;"
    echo $createDbQuery | mysql -u $mysqlUser -p
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Database created successfully." -ForegroundColor Green
    } else {
        Write-Host "✗ Error creating database. Please create manually." -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env file with your MySQL credentials" -ForegroundColor White
Write-Host "  2. Run: python app.py" -ForegroundColor White
Write-Host "  3. Open browser: http://localhost:5000" -ForegroundColor White
Write-Host "  4. Admin login: username='admin', password='admin123'" -ForegroundColor White
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  python app.py" -ForegroundColor White
Write-Host ""
