from sqlalchemy import delete, select, text, update
from sqlalchemy.orm import Session

from app.models.analytics.procedure import Procedure, ProcedureHistory


class ProcedureRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Procedure | None:
        row = self._session.get(Procedure, id)
        return row

    def get_all(self) -> list[Procedure]:
        rows = self._session.scalars(
            select(Procedure).order_by(Procedure.exec_order)
        ).all()
        return list(rows)

    def create(self, name: str, exec_order: int) -> int:
        row = Procedure(name=name, exec_order=exec_order, is_active=True)
        self._session.add(row)
        self._session.flush()  # fills row.id without ending the transaction
        return row.id

    def update(self, id: int, name: str, exec_order: int, is_active: bool) -> None:
        self._session.execute(
            update(Procedure)
            .where(Procedure.id == id)
            .values(name=name, exec_order=exec_order, is_active=is_active)
        )

    def delete(self, id: int) -> None:
        self._session.execute(delete(Procedure).where(Procedure.id == id))

    def run_by_name(self, name: str) -> None:
        # stays raw: it calls a stored procedure
        self._session.execute(text("EXEC dbo.ProcedureExecutor :name"), {"name": name})

    def exists_by_name(
        self,
        name: str,
        exclude_id: int | None = None,
    ) -> bool:
        cond = Procedure.name == name

        if exclude_id is not None:
            cond = cond & (Procedure.id != exclude_id)

        stmt = select(Procedure.id).where(cond).limit(1)
        return self._session.scalar(stmt) is not None

    def get_last_history_by_id(self, procedure_id: int) -> list[ProcedureHistory]:
        stmt = (
            select(ProcedureHistory)
            .where(ProcedureHistory.procedure_id == procedure_id)
            .order_by(ProcedureHistory.start_at.desc())
            .limit(10)  # rendered as TOP 10 on SQL Server
        )
        rows = self._session.scalars(stmt).all()
        return list(rows)
