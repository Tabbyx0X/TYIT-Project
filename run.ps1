# Quick Start Script
# This script activates the virtual environment and runs the application

Write-Host "Starting Online Voting System..." -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & ".\venv\Scripts\Activate.ps1"
    Write-Host "✓ Virtual environment activated." -ForegroundColor Green
} else {
    Write-Host "✗ Virtual environment not found. Please run setup.ps1 first." -ForegroundColor Red
    exit
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "✗ .env file not found. Please run setup.ps1 first." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Starting Flask application..." -ForegroundColor Yellow
Write-Host "Access the application at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run the application
python app.py
