"""
Script to create the first admin user.

Run with:
    uv run python scripts/create_admin.py
"""

import sys
from getpass import getpass
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.core.security import get_password_hash
from app.db.database import SessionLocal
from app.exceptions.exceptions import AlreadyExistsError
from app.repositories.user_repository import UserRepository


def create_admin_user():
    db = SessionLocal()
    repo = UserRepository(db)

    try:
        print("=== Create First Admin User ===\n")

        username = input("Username: ").strip().lower()

        if not username:
            print("❌ Username cannot be empty")
            return

        if repo.get_by_username(username):
            raise AlreadyExistsError("User", "username", username)

        password = getpass("Password: ")

        if not password:
            print("❌ Password cannot be empty")
            return

        password_confirm = getpass("Confirm Password: ")

        if password != password_confirm:
            print("❌ Passwords do not match")
            return

        user = repo.create(
            username,
            get_password_hash(password),
            is_admin=True,
        )

        print(f"\n✅ Admin user '{username}' created successfully!")
        db.commit()

        return user

    except AlreadyExistsError as e:
        print(f"\n❌ {e}")
    except Exception as e:
        print(f"\n❌ Error creating admin user: {e}")
    finally:
        db.close()
        pass


if __name__ == "__main__":
    create_admin_user()
