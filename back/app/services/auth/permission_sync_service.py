from sqlalchemy.orm import Session

from app.core.permisions import PermissionEnum
from app.repositories.auth.permission_repo import PermissionRepo
from app.services.common import WriteService


class PermissionSyncService(WriteService):
    def __init__(self, session: Session, repository: PermissionRepo) -> None:
        super().__init__(session)
        self._repository = repository

    def sync_permissions(self) -> dict[str, list[str]]:
        expected = {permission.value for permission in PermissionEnum}

        with self._write():
            existing = self._repository.get_names()
            created = sorted(expected - existing)
            already_exists = sorted(expected & existing)
            self._repository.add_names(created)

        return {"created": created, "already_exists": already_exists}
