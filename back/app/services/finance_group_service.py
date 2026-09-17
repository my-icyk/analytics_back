from app.domains.finance import (
    Division,
    Group,
    GroupDetail,
    GroupFilter,
    GroupPage,
    GroupType,
)
from app.exceptions.exceptions import (
    AlreadyExistsError,
    DeleteProtectedError,
    NotFoundError,
)
from app.repositories.division_repository import DivisionRepository
from app.repositories.group_repository import GroupRepository
from app.repositories.group_rule_repository import GroupRuleRepository
from app.repositories.group_type_repository import GroupTypeRepository

# TODO: De exclus de aici


class FinanceGroupService:
    def __init__(
        self,
        group_type_repository: GroupTypeRepository,
        division_repository: DivisionRepository,
        group_repository: GroupRepository,
        group_rule_repository: GroupRuleRepository,
    ):
        self.group_type_repository = group_type_repository
        self.division_repository = division_repository
        self.group_repository = group_repository
        self.group_rule_repository = group_rule_repository

    def get_groups_page(self, filters: GroupFilter) -> GroupPage:
        items = self.group_repository.get_all(filters)
        total = self.group_repository.count(filters)
        return GroupPage(items=items, total=total)

    def _validate_group_name(self, name: str):
        group = self.group_repository.get_by_name(name)
        if group:
            raise AlreadyExistsError("Group", "name", name)

    def _validate_division_name(self, name: str):
        division = self.division_repository.get_by_name(name)
        if division:
            raise AlreadyExistsError("Division", "name", name)

    def _validate_group_type(self, group_type_id: int):
        group_type = self.group_type_repository.get_by_id(group_type_id)
        if not group_type:
            raise NotFoundError("GroupType", "id", str(group_type_id))

    def _validate_division(self, division_id: int):
        existing_division = self.division_repository.get_by_id(division_id)
        if not existing_division:
            raise NotFoundError("Division", "id", str(division_id))

    def get_group_types(self) -> list[GroupType]:
        return self.group_type_repository.get_all()

    def get_divisions(self) -> list[Division]:
        return self.division_repository.get_all()

    def get_division(self, id: int) -> Division:
        division = self.division_repository.get_by_id(id)
        if not division:
            raise NotFoundError("Division", "id", str(id))
        return division

    def create_division(self, name: str) -> Division:
        self._validate_division_name(name)
        return self.division_repository.create(name)

    def update_division(self, id: int, name: str) -> Division:
        self.get_division(id)
        self._validate_division_name(name)

        return self.division_repository.update(id, name)

    def get_group(self, id: int) -> GroupDetail:
        group = self.group_repository.get_by_id(id)
        if not group:
            raise NotFoundError("Group", "id", str(id))
        return group

    def get_groups(
        self,
        filters: GroupFilter,
    ) -> list[GroupDetail]:
        return self.group_repository.get_all(filters)

    def count_groups(
        self,
        filters: GroupFilter,
    ) -> int:
        return self.group_repository.count(filters)

    def create_group(
        self, name: str, group_type_id: int, division_id: int
    ) -> GroupDetail:
        self._validate_group_name(name)

        self._validate_group_type(group_type_id)

        self._validate_division(division_id)
        group = self.group_repository.create(name, group_type_id, division_id)
        return self.get_group(group.id)

    def update_group(
        self, id: int, name: str, group_type_id: int, division_id: int
    ) -> GroupDetail:
        self.get_group(id)
        existing_group: Group | None = self.group_repository.get_by_name(name)

        if existing_group is not None and existing_group.id != id:
            raise AlreadyExistsError("Group", "name", name)

        self._validate_group_type(group_type_id)

        self._validate_division(division_id)
        group = self.group_repository.update(id, name, division_id, group_type_id)
        return self.get_group(group.id)

    def delete_group(self, id: int) -> None:
        group = self.group_repository.get_by_id_light(id)

        if not group:
            raise NotFoundError("Group", "id", str(id))
        existing_rules = self.group_rule_repository.get_by_group_id(id)

        if existing_rules:
            raise DeleteProtectedError(
                "Group", f'Group "{group.name}" has associated rules'
            )
        self.group_repository.delete(id)

    def delete_division(self, id: int) -> None:
        self.get_division(id)
        groups = self.group_repository.get_by_division_id_light(id)
        if groups:
            raise DeleteProtectedError(
                "Division",
                f'Division "{self.get_division(id).name}" has associated groups',
            )
        self.division_repository.delete(id)
