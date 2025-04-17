import os
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def create_admin_user(username, email, password, full_name):
    with app.app_context():
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"User {username} already exists!")
            return False
        
        # Create new admin user
        admin_user = User(
            username=username,
            email=email,
            full_name=full_name,
            role='admin'
        )
        admin_user.password_hash = generate_password_hash(password)
        
        # Add to database
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user {username} created successfully!")
        return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 5:
        print("Usage: python create_admin.py <username> <email> <password> <full_name>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    full_name = sys.argv[4]
    
    create_admin_user(username, email, password, full_name)