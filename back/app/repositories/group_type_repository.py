from app.api.v1.schemas.finance import GroupTypeDetails
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

    def get_all(self) -> list[GroupTypeDetails]:

        sql = """
            SELECT
                t.id,
                t.name,
                group_count = COUNT(g.id)
            FROM finance.dimGroupTypes AS t
            LEFT JOIN finance.dimGroups AS g ON g.group_type_id = t.id
            GROUP BY
                t.id,
                t.name
            ORDER BY
                t.id
        """
        results = self._fetch_all(sql)
        return [GroupTypeDetails.model_validate(result) for result in results]
