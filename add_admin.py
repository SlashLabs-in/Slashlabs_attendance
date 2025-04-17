from app import app, db
from models import User

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@example.com'
ADMIN_PASSWORD = 'admin123'
ADMIN_FULL_NAME = 'Admin User'

def create_admin():
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username=ADMIN_USERNAME).first()
        
        if admin:
            print(f"Admin user '{ADMIN_USERNAME}' already exists.")
            return
        
        # Create admin user
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            full_name=ADMIN_FULL_NAME,
            role='admin'
        )
        admin.set_password(ADMIN_PASSWORD)
        
        # Add to database
        db.session.add(admin)
        db.session.commit()
        
        print(f"Admin user created successfully!")
        print(f"Username: {ADMIN_USERNAME}")
        print(f"Password: {ADMIN_PASSWORD}")

if __name__ == '__main__':
    create_admin()