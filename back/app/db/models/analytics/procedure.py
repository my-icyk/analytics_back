from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Procedure(Base):
    __tablename__ = "ProcedureRunList"
    __table_args__ = {"schema": "dbo"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    exec_order: Mapped[int] = mapped_column(Integer)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_run: Mapped[datetime | None] = mapped_column(DateTime)
    last_status: Mapped[str] = mapped_column(
        String(50),
        default="not_run",
        server_default="not_run",
    )
    last_duration_ms: Mapped[int | None] = mapped_column(BigInteger)
    last_error: Mapped[str | None] = mapped_column(Text)


class ProcedureHistory(Base):
    __tablename__ = "ProcedureRunHistory"
    __table_args__ = {"schema": "dbo"}

    procedure_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_at: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    end_at: Mapped[datetime | None] = mapped_column(DateTime)
    execution_time_ms: Mapped[int | None] = mapped_column(BigInteger)
    status: Mapped[str | None] = mapped_column(String(50))
    error_detail: Mapped[str | None] = mapped_column(Text)
