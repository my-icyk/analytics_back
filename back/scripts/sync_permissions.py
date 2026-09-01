# TODO: Need to place it later in better place, maybe in a separate script or as part of an initialization process
from sqlalchemy import text

from app.core.permisions import PermissionEnum
from app.db.database import SessionLocal


def sync_permissions() -> dict[str, list[str]]:
    db = SessionLocal()

    try:
        # Get existing permissions
        result = db.execute(
            text("""
                SELECT name
                FROM api.permissions
            """)
        )

        existing_permissions = {row[0] for row in result.fetchall()}

        # Get enum permissions
        enum_permissions = {permission.value for permission in PermissionEnum}

        # Find missing permissions
        missing_permissions = enum_permissions - existing_permissions

        # Insert missing permissions
        for permission in missing_permissions:
            db.execute(
                text("""
                    INSERT INTO api.permissions (name)
                    VALUES (:name)
                """),
                {"name": permission},
            )

        db.commit()

        return {
            "created": list(missing_permissions),
            "already_exists": list(enum_permissions & existing_permissions),
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def main():
    print("Starting permissions synchronization...")
    result = sync_permissions()
    print("Permissions synchronization completed.")
    print(f"Created permissions: {result['created']}")
    print(f"Already existing permissions: {result['already_exists']}")


if __name__ == "__main__":
    main()
