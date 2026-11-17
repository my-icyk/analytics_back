from datetime import date

from sqlalchemy.orm import Session

from app.db.models.finance import (
    Company,
    Department,
    DepartmentRepartition,
    Division,
    Group,
    GroupType,
)
from app.domains.user import User
from app.exceptions.exceptions import (
    AlreadyExistsError,
    DeleteProtectedError,
    NotFoundError,
)
from app.filters.finance import DepartmentRepartitionFilter, GroupFilter
from app.repositories.base import LookupResponse
from app.repositories.finance import (
    CompanyRepo,
    DepartmentRepartitionRepo,
    DepartmentRepo,
    DivisionRepo,
    GroupRepo,
    GroupRuleRepo,
    GroupTypeRepo,
)
from app.services.common import WriteService

# TODO: De exclus de aici


class FinanceGroupService(WriteService):
    def __init__(
        self,
        session: Session,
        *,
        group_type_repo: GroupTypeRepo,
        division_repo: DivisionRepo,
        group_repo: GroupRepo,
        group_rule_repo: GroupRuleRepo,
        department_repo: DepartmentRepo,
        department_repartition_repo: DepartmentRepartitionRepo,
        company_repo: CompanyRepo,
    ) -> None:
        super().__init__(session)
        self._group_types = group_type_repo
        self._divisions = division_repo
        self._groups = group_repo
        self._rules = group_rule_repo
        self._departments = department_repo
        self._department_repartitions = department_repartition_repo
        self._companies = company_repo

    def get_company(self, company_id: int) -> Company:
        company = self._companies.get_company(company_id)
        if company is None:
            raise NotFoundError("Company", "id", str(company_id))
        return company

    def get_companies(self, only_active: bool = True) -> list[Company]:
        return self._companies.get_companies(only_active)

    def get_groups_page(self, filters: GroupFilter) -> tuple[list[Group], int]:
        return self._groups.get_all(filters)

    def _validate_group_name(self, name: str):
        group = self._groups.get_by_name(name)
        if group:
            raise AlreadyExistsError("Group", "name", name)

    def _validate_division_name(self, name: str):
        division = self._divisions.get_by_name(name)
        if division:
            raise AlreadyExistsError("Division", "name", name)

    def _validate_group_type(self, group_type_id: int):
        group_type = self._group_types.get_by_id(group_type_id)
        if not group_type:
            raise NotFoundError("GroupType", "id", str(group_type_id))

    def _validate_division(self, division_id: int):
        existing_division = self._divisions.get_by_id(division_id)
        if not existing_division:
            raise NotFoundError("Division", "id", str(division_id))

    def get_group_types(self) -> list[GroupType]:
        return self._group_types.get_all()

    def get_divisions(self) -> list[Division]:
        return self._divisions.get_all()

    def get_division(self, id: int) -> Division:
        division = self._divisions.get_by_id(id)
        if not division:
            raise NotFoundError("Division", "id", str(id))
        return division

    def get_folders(self) -> list[Group]:
        return self._groups.get_folders()

    def create_division(
        self, name: str, is_administrative: bool, company_id: int
    ) -> int:
        with self._write():
            division_id = self._divisions.create(name, is_administrative, company_id)
        return division_id

    def update_division(
        self, id: int, name: str, is_administrative: bool, company_id: int
    ) -> None:
        with self._write():
            division = self.get_division(id)
            division.name = name
            division.is_administrative = is_administrative
            division.company_id = company_id

    def get_group(self, id: int) -> Group:
        group = self._groups.get_by_id(id)
        if not group:
            raise NotFoundError("Group", "id", str(id))
        return group

    def create_group(
        self,
        name: str,
        group_type_id: int,
        division_id: int,
        parent_id: int | None = None,
    ) -> int:
        with self._write():
            self._validate_group_name(name)
            self._validate_group_type(group_type_id)
            self._validate_division(division_id)

            group_id = self._groups.create(
                name=name,
                group_type_id=group_type_id,
                division_id=division_id,
                parent_id=parent_id,
            )
        return group_id

    def update_group(
        self,
        id: int,
        name: str,
        group_type_id: int,
        division_id: int,
        parent_id: int | None = None,
    ) -> None:
        with self._write():
            group = self._groups.get_by_id_light(id)
            if group is None:
                raise NotFoundError("Group", "id", str(id))

            existing = self._groups.get_by_name(name)
            if existing is not None and existing.id != group.id:
                raise AlreadyExistsError("Group", "name", name)

            self._validate_group_type(group_type_id)
            self._validate_division(division_id)

            group.name = name
            group.group_type_id = group_type_id
            group.division_id = division_id
            group.parent_id = parent_id

    def delete_group(self, id: int) -> None:
        with self._write():
            group = self._groups.get_by_id_light(id)
            if group is None:
                raise NotFoundError("Group", "id", str(id))

            if self._rules.get_by_group_id(id):
                raise DeleteProtectedError(
                    "Group",
                    f'Group "{group.name}" has associated rules',
                )

            self._groups.delete(group)

    def delete_division(self, id: int) -> None:
        with self._write():
            division = self.get_division(id)
            if division.group_count > 0:
                raise DeleteProtectedError(
                    "Division",
                    f'Division "{division.name}" has associated groups',
                )
            self._divisions.delete(division)

    def list_department_repartitions(
        self, caller: User, filters: DepartmentRepartitionFilter
    ) -> tuple[list[DepartmentRepartition], int]:
        return self._department_repartitions.get_all(filters)

    def get_department_repartition(self, group_id: int) -> list[DepartmentRepartition]:
        self.get_group(group_id)
        return self._department_repartitions.get_by_group_id(group_id)

    def create_department_repartition(
        self, department_id: int, group_id: int, valid_from: date, valid_to: date | None
    ) -> int:
        with self._write():
            self.get_group(group_id)
            repartition_id = self._department_repartitions.create(
                department_id, group_id, valid_from, valid_to
            )
        return repartition_id

    def _get_repartition_for_group(
        self, id: int, group_id: int
    ) -> DepartmentRepartition:
        row = self._department_repartitions.get_for_group(id, group_id)
        if row is None:
            raise NotFoundError("DepartmentRepartition", "id", str(id))
        return row

    def update_department_repartition(
        self,
        id: int,
        department_id: int,
        group_id: int,
        valid_from: date,
        valid_to: date | None,
    ) -> None:
        with self._write():
            row = self._get_repartition_for_group(id, group_id)
            row.department_id = department_id
            row.valid_from = valid_from
            row.valid_to = valid_to

    def delete_department_repartition(self, id: int, group_id: int) -> None:
        with self._write():
            row = self._get_repartition_for_group(id, group_id)
            self._department_repartitions.delete(row)

    def get_departments(self) -> list[Department]:
        return self._departments.get_all()

    def lookup_groups(self, search: str | None) -> list[LookupResponse]:
        return self._groups.lookup(search)

    def lookup_departments(self, search: str | None) -> list[LookupResponse]:
        return self._departments.lookup(search)
