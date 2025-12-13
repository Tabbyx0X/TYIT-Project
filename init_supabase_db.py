# Initialize Supabase Database
from app import app, db, Admin

def init_database():
    """Create database tables and default admin"""
    with app.app_context():
        print("🔄 Creating database tables...")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create default admin if doesn't exist
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                email='admin@voting.com',
                role='admin'
            )
            admin.set_password('Admin@123')
            db.session.add(admin)
            db.session.commit()
            
            print("\n✅ Default admin created!")
            print("   Username: admin")
            print("   Password: Admin@123")
            print("\n⚠️  Remember to change the password after first login!")
        else:
            print("ℹ️  Admin already exists")
        
        print("\n🎉 Database initialization complete!")
        print("   You can now run: python app.py")

if __name__ == '__main__':
    init_database()
