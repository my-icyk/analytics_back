from app.domains.analytics import Procedure, ProcedureHistory
from app.exceptions.exceptions import AlreadyExistsError
from app.repositories.analytics import ProcedureRepository


class ProcedureService:
    def __init__(self, procedure_repository: ProcedureRepository):
        self._procedure_repository = procedure_repository

    def _validate_name(self, name: str, exclude_id: int | None = None):
        if self._procedure_repository.exists_by_name(name, exclude_id=exclude_id):
            raise AlreadyExistsError(entity="Procedure", field="name", value=name)

    def get_all(self) -> list[Procedure]:
        return self._procedure_repository.get_all()

    def get_by_id(self, id: int) -> Procedure:
        procedure = self._procedure_repository.get_by_id(id)
        if not procedure:
            raise ValueError(f"Procedure with id {id} not found")

        return procedure

    def run_by_id(self, id: int):
        procedure = self.get_by_id(id)

        return self._procedure_repository.run_by_id(procedure.name)

    def create(self, name: str, exec_order: int):
        self._validate_name(name)
        return self._procedure_repository.create(name, exec_order)

    def update(self, id: int, name: str, exec_order: int, is_active: bool):
        self._validate_name(name, exclude_id=id)

        return self._procedure_repository.update(id, name, exec_order, is_active)

    def delete(self, id: int):
        self.get_by_id(id)

        return self._procedure_repository.delete(id)

    def get_last_history_by_id(self, procedure_id: int) -> list[ProcedureHistory]:
        self.get_by_id(procedure_id)

        return self._procedure_repository.get_last_history_by_id(procedure_id)
