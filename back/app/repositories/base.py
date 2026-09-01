"""
Thin base repository. Unlike an ORM-based repository, this does NOT provide
generic get/create/update/delete — with raw SQL, every table's statements are
different, so trying to genericize them fights you more than it helps.

What IS shared and worth centralizing: running a statement and turning rows
into plain dicts, ready to hand to a Pydantic schema.
"""

from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def _fetch_one(self, sql: str, params: dict[str, Any]) -> dict | None:
        row = self.db.execute(text(sql), params).mappings().first()
        return dict(row) if row is not None else None

    def _fetch_all(self, sql: str, params: dict[str, Any]) -> list[dict]:
        rows = self.db.execute(text(sql), params).mappings().all()
        return [dict(r) for r in rows]

    def _execute(self, sql: str, params: dict[str, Any]) -> int:
        """For statements with no OUTPUT clause (e.g. plain DELETE). Returns rowcount."""
        result = self.db.execute(text(sql), params)
        return result.rowcount
