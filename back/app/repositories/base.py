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
    PERMISSIONS = "api.sp_lookup_permissions"
    USERS = "api.sp_lookup_users"
    ROLES = "api.sp_lookup_roles"
    DIVISIONS = "api.sp_lookup_divisions"


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def _fetch_one_or_none(self, sql: str, params: dict[str, Any]) -> dict | None:
        row = self.db.execute(text(sql), params).mappings().first()
        return dict(row) if row is not None else None

    def _fetch_one(self, sql: str, params: dict[str, Any]) -> dict:
        row = self._fetch_one_or_none(sql, params)
        # TODO: To review later comment
        assert row is not None, "Expected exactly one row"
        return dict(row)

    def _fetch_all(self, sql: str, params: dict[str, Any] | None = None) -> list[dict]:
        rows = self.db.execute(text(sql), params or {}).mappings().all()
        return [dict(r) for r in rows]

    def _execute(self, sql: str, params: dict[str, Any]) -> None:
        self.db.execute(text(sql), params)

    def _scalar(
        self,
        sql: str,
        params: dict[str, Any] | None = None,
        expanding: list[str] | None = None,
    ) -> Any:
        stmt = text(sql)
        if expanding:
            stmt = stmt.bindparams(
                *[bindparam(name, expanding=True) for name in expanding]
            )
        return self.db.execute(stmt, params or {}).scalar()

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
