"""
Script to update the user token in the database
Run this script to update the token for user ID 10 (JMart)
Requires WORKING_TOKEN in .env (same directory as config.py).
"""
import os

from app import app, db
from models.user_model import User

WORKING_TOKEN = os.environ.get("WORKING_TOKEN")

def update_token():
    if not WORKING_TOKEN:
        print("Missing WORKING_TOKEN. Set it in .env next to config.py.")
        return
    with app.app_context():
        # Find user with UserId = 10
        user = User.query.filter_by(UserId=10).first()
        
        if user:
            print(f"Found user: {user.Username} (ID: {user.UserId})")
            print(f"Current token length: {len(user.Token) if user.Token else 0}")
            print(f"Current token preview: {user.Token[:50] if user.Token else 'None'}...")
            
            # Update the token
            user.Token = WORKING_TOKEN
            db.session.commit()
            
            print(f"\nToken updated successfully!")
            print(f"New token length: {len(user.Token)}")
            print(f"New token preview: {user.Token[:50]}...")
        else:
            print("User with ID 10 not found!")

if __name__ == "__main__":
    update_token()
