"""
Thin base repository. Unlike an ORM-based repository, this does NOT provide
generic get/create/update/delete — with raw SQL, every table's statements are
different, so trying to genericize them fights you more than it helps.

What IS shared and worth centralizing: running a statement and turning rows
into plain dicts, ready to hand to a Pydantic schema.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel
from sqlalchemy import bindparam, text
from sqlalchemy.orm import Session


class LookupResponse(BaseModel):
    value: int
    label: str


class LookupObjects(Enum):
    USERS = "api.sp_lookup_users"
    DEPARTMENTS = "api.sp_lookup_departments"
    GROUPS = "api.sp_lookup_groups"


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def _build_stmt(self, sql: str, params: dict[str, Any] | None = None):
        stmt = text(sql)
        list_params = [
            bindparam(key, expanding=True)
            for key, value in (params or {}).items()
            if isinstance(value, (list, tuple))
        ]
        return stmt.bindparams(*list_params) if list_params else stmt

    def _run(self, sql: str, params: dict[str, Any] | None = None):
        params = params or {}
        return self.db.execute(self._build_stmt(sql, params), params)

    def _fetch_one_or_none(self, sql: str, params: dict[str, Any]) -> dict | None:
        row = self.db.execute(text(sql), params).mappings().first()
        return dict(row) if row is not None else None

    def _fetch_one(self, sql: str, params: dict[str, Any]) -> dict:
        row = self._fetch_one_or_none(sql, params)
        # TODO: To review later comment
        assert row is not None, "Expected exactly one row"
        return dict(row)

    def _fetch_all(self, sql: str, params: dict[str, Any] | None = None) -> list[dict]:
        return [dict(r) for r in self._run(sql, params).mappings().all()]

    def _scalar(self, sql: str, params: dict[str, Any] | None = None) -> Any:
        return self._run(sql, params).scalar()

    def _execute(self, sql: str, params: dict[str, Any] | None = None) -> None:
        self._run(sql, params)

    def _update(self, sql: str, params: dict[str, Any]) -> dict:
        row = self._fetch_one_or_none(sql, params)
        assert row is not None, "UPDATE with OUTPUT should always return a row"
        return dict(row)

    def _fetch_some(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        expanding: list[str] | None = None,
    ) -> list[dict]:
        stmt = text(sql)
        if expanding:
            stmt = stmt.bindparams(
                *[bindparam(name, expanding=True) for name in expanding]
            )
        rows = self.db.execute(stmt, params or {}).mappings().all()
        return [dict(r) for r in rows]

    def _lookup(self, obj: LookupObjects, search: str) -> list[LookupResponse]:
        sql = f"exec {obj.value} @search = :search"
        rows = self._fetch_all(sql, {"search": search})
        return [LookupResponse.model_validate(row) for row in rows]
