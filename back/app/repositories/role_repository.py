from app.domains.role import Role
from app.repositories.base import BaseRepository, LookupObjects, LookupResponse


class RoleRepository(BaseRepository):
    def get_by_id(self, role_id: int) -> Role | None:
        sql = """
            SELECT *
            FROM api.roles
            WHERE id = :id
        """

        row = self._fetch_one_or_none(sql, {"id": role_id})

        return Role.model_validate(row) if row else None

    def get_all(
        self, name: str | None, limit: int, offset: int
    ) -> tuple[list[Role], int]:
        where = ""
        params: dict = {}

        if name:
            where = "WHERE UPPER(name) LIKE UPPER(:name)"
            params["name"] = f"%{name}%"

        rows = self._fetch_all(
            f"""
            SELECT id, name, description
            FROM api.roles
            {where}
            ORDER BY id
            OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
            """,
            {**params, "limit": limit, "offset": offset},
        )

        total = self._fetch_one(
            f"SELECT COUNT(*) AS total FROM api.roles {where}",
            params,
        )["total"]

        return [Role.model_validate(row) for row in rows], total

    def create(self, name: str, description: str | None = None) -> Role:
        sql = """
            INSERT INTO api.roles (name, description)
            OUTPUT INSERTED.*
            VALUES (:name, :description)
        """
        role = self._fetch_one_or_none(sql, {"name": name, "description": description})

        return Role.model_validate(role)

    def update(self, role_id: int, name: str, description: str | None) -> Role:
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
        return Role.model_validate(role)

    def get_by_name(self, name: str) -> Role | None:
        sql = """
            SELECT *
            FROM api.roles
            WHERE name = :name
        """
        row = self._fetch_one_or_none(sql, {"name": name})

        return Role.model_validate(row) if row else None

    def delete(self, role_id: int) -> None:
        sql = """
            DELETE FROM api.roles
            WHERE id = :id
        """
        self._execute(sql, {"id": role_id})

    def lookup(self, search: str) -> list[LookupResponse]:
        return self._lookup(LookupObjects.ROLES, search)
