from app.domains.finance import GroupType
from app.repositories.base import BaseRepository


class GroupTypeRepository(BaseRepository):
    def get_by_id(self, id) -> GroupType | None:

        sql = """
            SELECT
                id,
                name
            FROM finance.dimGroupTypes
            WHERE
                id = :id
        """
        result = self._fetch_one_or_none(sql, {"id": id})
        return GroupType.model_validate(result) if result else None

    def get_all(self) -> list[GroupType]:

        sql = """
            SELECT
                id,
                name
            FROM finance.dimGroupTypes
        """
        results = self._fetch_all(sql)
        return [GroupType.model_validate(result) for result in results]

    def create(self, name) -> GroupType:

        sql = """
            INSERT INTO finance.dimGroupTypes (name)
            OUTPUT INSERTED.*
            VALUES (:name)
        """
        result = self._fetch_one(sql, {"name": name})
        return GroupType.model_validate(result)

    def update(self, id, name) -> GroupType:
        sql = """
            UPDATE finance.dimGroupTypes
            SET name = :name
            OUTPUT INSERTED.*
            WHERE id = :id
        """
        result = self._fetch_one(sql, {"id": id, "name": name})
        return GroupType.model_validate(result)

    def delete(self, id) -> None:

        sql = """
            DELETE FROM finance.dimGroupTypes  
            WHERE id = :id
        """
        self._execute(sql, {"id": id})
