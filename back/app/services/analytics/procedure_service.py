from app.db.models.analytics import Procedure, ProcedureHistory
from app.exceptions.exceptions import AlreadyExistsError, NotFoundError
from app.repositories.analytics import ProcedureRepository


class ProcedureService:
    def __init__(self, procedure_repository: ProcedureRepository):
        self._procedure_repo = procedure_repository

    def _validate_name(self, name: str, exclude_id: int | None = None) -> None:
        if self._procedure_repo.exists_by_name(name, exclude_id=exclude_id):
            raise AlreadyExistsError(entity="Procedure", field="name", value=name)

    def get_all(self) -> list[Procedure]:
        return self._procedure_repo.get_all()

    def get_by_id(self, id: int) -> Procedure:
        procedure = self._procedure_repo.get_by_id(id)
        if procedure is None:
            raise NotFoundError(entity="Procedure", field="id", value=str(id))
        return procedure

    def run_by_id(self, id: int) -> None:
        procedure = self.get_by_id(id)
        self._procedure_repo.run_by_name(procedure.name)

    def create(self, name: str, exec_order: int) -> int:
        self._validate_name(name)
        return self._procedure_repo.create(name, exec_order)

    def update(self, id: int, name: str, exec_order: int, is_active: bool) -> None:
        self.get_by_id(id)
        self._validate_name(name, exclude_id=id)
        self._procedure_repo.update(id, name, exec_order, is_active)

    def delete(self, id: int) -> None:
        self.get_by_id(id)
        self._procedure_repo.delete(id)

    def get_last_history_by_id(self, procedure_id: int) -> list[ProcedureHistory]:
        self.get_by_id(procedure_id)
        return self._procedure_repo.get_last_history_by_id(procedure_id)
