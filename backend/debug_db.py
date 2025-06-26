from app.database import get_session
from app.simple_auth import create_demo_user
from app.models import User
from sqlmodel import select

print("Testing database connection...")

try:
    db = next(get_session())
    print("Database connection successful!")
    
    # Check if demo user exists
    demo_user = db.exec(select(User).where(User.email == "demo@example.com")).first()
    if demo_user:
        print(f"Demo user already exists: {demo_user.email}")
    else:
        print("Demo user does not exist, creating...")
        create_demo_user(db)
        print("Demo user created successfully!")
        
    # List all users
    users = db.exec(select(User)).all()
    print(f"Total users in database: {len(users)}")
    for user in users:
        print(f"  - {user.email} (ID: {user.id})")
        
except Exception as e:
    print(f"Database error: {e}")
    import traceback
    traceback.print_exc() 