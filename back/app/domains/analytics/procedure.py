from datetime import datetime

from app.domains.domain_model import DomainModel


class Procedure(DomainModel):
    id: int
    name: str
    exec_order: int
    is_active: bool
    last_run: datetime | None = None
    last_status: str | None = None
    last_duration_ms: int | None = None
    last_error: str | None = None


class ProcedureHistory(DomainModel):
    procedure_id: int
    start_at: datetime
    end_at: datetime | None = None
    execution_time_ms: int | None = None
    status: str | None = None
    error_detail: str | None = None
