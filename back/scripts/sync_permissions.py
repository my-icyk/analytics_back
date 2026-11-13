from app.db.database import SessionLocal
from app.repositories.auth.permision_repository import PermissionRepository
from app.services.auth.permission_sync_service import PermissionSyncService


def main() -> None:
    with SessionLocal() as db:
        service = PermissionSyncService(db, PermissionRepository(db))
        result = service.sync_permissions()

    print("Permissions synchronization completed.")
    print(f"Created permissions: {result['created']}")
    print(f"Already existing permissions: {result['already_exists']}")


if __name__ == "__main__":
    main()
