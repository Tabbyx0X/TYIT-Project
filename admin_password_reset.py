"""
Admin Password Reset Script
This script allows you to change the admin password directly from the command line.
Useful if you've forgotten your password or need to reset it.
"""

from app import app, db, Admin
from werkzeug.security import generate_password_hash
import sys

def change_admin_password():
    """Change admin password via command line"""
    with app.app_context():
        print("\n" + "="*50)
        print("     ADMIN PASSWORD RESET UTILITY")
        print("="*50 + "\n")
        
        # Get username
        username = input("Enter admin username (default: admin): ").strip()
        if not username:
            username = "admin"
        
        # Find admin
        admin = Admin.query.filter_by(username=username).first()
        
        if not admin:
            print(f"\n❌ Error: Admin user '{username}' not found!")
            print("\nAvailable admin users:")
            admins = Admin.query.all()
            for a in admins:
                print(f"   - {a.username} ({a.email})")
            sys.exit(1)
        
        print(f"\n✓ Found admin: {admin.username} ({admin.email})")
        
        # Get new password
        new_password = input("\nEnter new password (min 6 characters): ").strip()
        
        if len(new_password) < 6:
            print("\n❌ Error: Password must be at least 6 characters long!")
            sys.exit(1)
        
        # Confirm password
        confirm_password = input("Confirm new password: ").strip()
        
        if new_password != confirm_password:
            print("\n❌ Error: Passwords do not match!")
            sys.exit(1)
        
        # Update password
        try:
            admin.set_password(new_password)
            db.session.commit()
            print("\n" + "="*50)
            print("✅ PASSWORD CHANGED SUCCESSFULLY!")
            print("="*50)
            print(f"\nUsername: {admin.username}")
            print(f"New Password: {new_password}")
            print("\n⚠️  Please keep this password safe and secure!")
            print("\n" + "="*50 + "\n")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error changing password: {str(e)}")
            sys.exit(1)


def list_admins():
    """List all admin users"""
    with app.app_context():
        admins = Admin.query.all()
        print("\n" + "="*50)
        print("     ADMIN USERS LIST")
        print("="*50 + "\n")
        
        if not admins:
            print("No admin users found.")
        else:
            for i, admin in enumerate(admins, 1):
                print(f"{i}. Username: {admin.username}")
                print(f"   Email: {admin.email}")
                print(f"   Created: {admin.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print()
        
        print("="*50 + "\n")


def create_new_admin():
    """Create a new admin user"""
    with app.app_context():
        print("\n" + "="*50)
        print("     CREATE NEW ADMIN USER")
        print("="*50 + "\n")
        
        username = input("Enter username: ").strip()
        email = input("Enter email: ").strip()
        password = input("Enter password (min 6 characters): ").strip()
        confirm_password = input("Confirm password: ").strip()
        
        # Validation
        if not all([username, email, password]):
            print("\n❌ Error: All fields are required!")
            sys.exit(1)
        
        if len(password) < 6:
            print("\n❌ Error: Password must be at least 6 characters long!")
            sys.exit(1)
        
        if password != confirm_password:
            print("\n❌ Error: Passwords do not match!")
            sys.exit(1)
        
        # Check if username exists
        if Admin.query.filter_by(username=username).first():
            print(f"\n❌ Error: Username '{username}' already exists!")
            sys.exit(1)
        
        # Check if email exists
        if Admin.query.filter_by(email=email).first():
            print(f"\n❌ Error: Email '{email}' already in use!")
            sys.exit(1)
        
        # Create admin
        try:
            admin = Admin(username=username, email=email)
            admin.set_password(password)
            db.session.add(admin)
            db.session.commit()
            
            print("\n" + "="*50)
            print("✅ ADMIN USER CREATED SUCCESSFULLY!")
            print("="*50)
            print(f"\nUsername: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")
            print("\n" + "="*50 + "\n")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error creating admin: {str(e)}")
            sys.exit(1)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("     ADMIN MANAGEMENT UTILITY")
    print("="*50)
    print("\nWhat would you like to do?")
    print("1. Change admin password")
    print("2. List all admin users")
    print("3. Create new admin user")
    print("0. Exit")
    print()
    
    choice = input("Enter your choice (0-3): ").strip()
    
    if choice == '1':
        change_admin_password()
    elif choice == '2':
        list_admins()
    elif choice == '3':
        create_new_admin()
    elif choice == '0':
        print("\nExiting...\n")
        sys.exit(0)
    else:
        print("\n❌ Invalid choice!")
        sys.exit(1)
