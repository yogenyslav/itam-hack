from src.data.repository import AbstractRepository
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.tags.model import Skill, Role, TeamGoal
from src.tags.domain import RoleCreate, TeamGoalCreate, SkillCreate


class TagsRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = get_logger("TagsRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(TagsRepository, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        roles_data: list[RoleCreate] | None = None,
        goals_data: list[TeamGoalCreate] | None = None,
        skills_data: list[SkillCreate] | None = None,
    ) -> int:
        if roles_data:
            return self.add_roles(roles_data)
        if goals_data:
            return self.add_goals(goals_data)
        if skills_data:
            return self.add_skills(skills_data)

    def get(
        self,
        roles: bool = False,
        goals: bool = False,
        skills: bool = False,
    ) -> list[Role | TeamGoal | Skill]:
        if roles:
            return self.get_all_roles()
        if goals:
            return self.get_all_goals()
        if skills:
            return self.get_all_skills()

    def update(self):
        ...

    def delete(self):
        ...

    def get_all(self):
        ...

    def add_roles(self, roles_data: list[RoleCreate]) -> int:
        roles = [Role(**role.model_dump()) for role in roles_data]
        self.db.session.add_all(roles)
        self.db.session.commit()

        return len(roles)

    def get_all_roles(self) -> list[Role]:
        return self.db.session.query(Role).all()

    def add_goals(self, goals_data: list[TeamGoalCreate]) -> int:
        goals = [TeamGoal(**goal.model_dump()) for goal in goals_data]
        self.db.session.add_all(goals)
        self.db.session.commit()

        return len(goals)

    def get_all_goals(self) -> list[TeamGoal]:
        return self.db.session.query(TeamGoal).all()

    def add_skills(self, skills_data: list[SkillCreate]) -> int:
        skills = [Skill(**skill.model_dump()) for skill in skills_data]
        self.db.session.add_all(skills)
        self.db.session.commit()

        return len(skills)

    def get_all_skills(self) -> list[Skill]:
        return self.db.session.query(Skill).all()