"""Create an admin user. Run from back/: uv run python scripts/create_admin.py"""

import sys
from getpass import getpass
from pathlib import Path

# Allow direct execution from the scripts directory.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.database import SessionLocal
from app.exceptions.exceptions import AlreadyExistsError, PasswordMismatchError
from app.repositories.auth import UserRepository
from app.services.auth import UserService
from app.services.common import Conflict


def main() -> int:
    print("Create admin user")

    username = input("Username: ").strip().lower()
    if not username:
        print("Username cannot be empty.", file=sys.stderr)
        return 1

    name = input(f"Display name [{username}]: ").strip() or username

    password = getpass("Password: ")
    if password != getpass("Confirm password: "):
        print("Passwords do not match.", file=sys.stderr)
        return 1

    try:
        with SessionLocal() as db:
            service = UserService(session=db, user_repository=UserRepository(db))
            service.create_admin_user(username=username, password=password, name=name)
    except (AlreadyExistsError, PasswordMismatchError, ValueError) as exc:
        print(f"Could not create admin: {exc}", file=sys.stderr)
        return 1
    except Conflict as exc:
        print(f"Could not create admin: {exc.detail}", file=sys.stderr)
        return 1

    print(f"Admin user '{username}' created successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
