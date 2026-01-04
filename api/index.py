import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

# Create all database tables on startup
with app.app_context():
    db.create_all()

# Export the Flask app directly for Vercel
# Vercel expects the WSGI application to be named 'app'
app = app
