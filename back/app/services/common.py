from collections.abc import Generator
from contextlib import contextmanager

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


class Conflict(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)


class WriteService:
    """Owns the write transaction; repositories never commit.

    Use a request-scoped Session with no unrelated pending writes. This supports
    an already-open read transaction from authentication; do not nest begin().
    """

    def __init__(self, session: Session):
        self._session = session

    @contextmanager
    def _write(self) -> Generator[None, None, None]:
        try:
            yield
            self._session.commit()
        except IntegrityError as error:
            self._session.rollback()
            raise Conflict(
                "The operation conflicts with related data or a database constraint"
            ) from error
        except Exception:
            self._session.rollback()
            raise
