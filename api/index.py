import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Admin

# Create all database tables and default admin on startup
with app.app_context():
    db.create_all()
    
    # Create default admin if not exists
    if not Admin.query.filter_by(username='ppatki').first():
        admin = Admin(
            username='ppatki',
            email='prasadpatki4@gmail.com',
            role='admin'
        )
        admin.set_password('ppatki16')
        db.session.add(admin)
        db.session.commit()
    
    # Create second admin if not exists
    if not Admin.query.filter_by(username='ppatki2').first():
        admin2 = Admin(
            username='ppatki2',
            email='prasadpatki84@gmail.com',
            role='admin'
        )
        admin2.set_password('ppatki16')
        db.session.add(admin2)
        db.session.commit()

# Export the Flask app directly for Vercel
# Vercel expects the WSGI application to be named 'app'
app = app
