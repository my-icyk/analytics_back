from sqlalchemy import Identity, Integer, String, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Department(Base):
    __tablename__ = "dimDepartments"
    __table_args__ = {"schema": "finance"}

    id: Mapped[int] = mapped_column(
        Integer, Identity(start=1, increment=1), primary_key=True
    )
    name: Mapped[str | None] = mapped_column(Unicode(255))
    ref: Mapped[str] = mapped_column(String(32), unique=True)
    code: Mapped[str | None] = mapped_column(String(100))
    brand: Mapped[str | None] = mapped_column(String(100))
