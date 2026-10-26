from app.domains.role import RoleWithCounts
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository):
    def get_by_id(self, role_id: int) -> RoleWithCounts | None:
        sql = """
            SELECT
				main.id,
				main.name,
				main.description,
				main.created_at,
				users_count = (SELECT COUNT(*) FROM API.user_roles AS notmain WHERE notmain.role_id = main.id),
				permissions_count = (SELECT COUNT(*) FROM API.role_permissions AS notmain WHERE notmain.role_id = main.id)
            FROM api.roles AS main
            WHERE
                main.id = :id
        """

        row = self._fetch_one_or_none(sql, {"id": role_id})

        return RoleWithCounts.model_validate(row) if row else None

    def get_all(self) -> list[RoleWithCounts]:

        rows = self._fetch_all(
            """
            SELECT
				main.id,
				main.name,
				main.description,
				main.created_at,
				users_count = (SELECT COUNT(*) FROM API.user_roles AS notmain WHERE notmain.role_id = main.id),
				permissions_count = (SELECT COUNT(*) FROM API.role_permissions AS notmain WHERE notmain.role_id = main.id)
            FROM api.roles AS main
            ORDER BY
                main.name 

            """
        )

        return [RoleWithCounts.model_validate(row) for row in rows]

    def create(self, name: str, description: str | None = None) -> RoleWithCounts:
        sql = """
            INSERT INTO api.roles (name, description)
            OUTPUT INSERTED.*
            VALUES (:name, :description)
        """
        role = self._fetch_one_or_none(sql, {"name": name, "description": description})

        return RoleWithCounts.model_validate(role)

    def update(
        self, role_id: int, name: str, description: str | None
    ) -> RoleWithCounts:
        sql = """
            UPDATE api.roles SET
                name = :name,
                description = :description
            OUTPUT INSERTED.*
            WHERE id = :id
        """
        role = self._fetch_one_or_none(
            sql, {"id": role_id, "name": name, "description": description}
        )
        return RoleWithCounts.model_validate(role)

    def get_by_name(self, name: str) -> RoleWithCounts | None:
        sql = """
            SELECT *
            FROM api.roles
            WHERE name = :name
        """
        row = self._fetch_one_or_none(sql, {"name": name})

        return RoleWithCounts.model_validate(row) if row else None

    def delete(self, role_id: int) -> None:
        sql = """
            DELETE FROM api.roles
            WHERE id = :id
        """
        self._execute(sql, {"id": role_id})

    def assign_permissions(
        self,
        role_id: int,
        permission_ids: list[int],
    ) -> None:
        self._execute(
            "DELETE FROM api.role_permissions WHERE role_id = :role_id",
            {"role_id": role_id},
        )

        if not permission_ids:
            return

        add_sql = """
            INSERT INTO api.role_permissions (role_id, permission_id)
            SELECT :role_id, id
            FROM api.permissions
            WHERE id IN :permission_ids
            """
        self._execute(
            add_sql,
            {"role_id": role_id, "permission_ids": permission_ids},
        )

    def get_existing_ids(self, ids: list[int]) -> set[int]:
        if not ids:
            return set()

        sql = """
            SELECT id
            FROM api.roles
            WHERE id IN :ids
        """
        rows = self._fetch_all(sql, {"ids": ids})
        return {row["id"] for row in rows}
