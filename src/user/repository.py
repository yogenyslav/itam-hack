from src.data.repository import AbstractRepository
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.user.model import User, Skill, Role, TeamGoal
from src.user.domain import UserDto, SurveyCreate
from src.auth.domain import Signup


class UserRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = get_logger("UserRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(UserRepository, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        user_data: Signup,
    ) -> User:
        user = User(**user_data.model_dump())
        self.db.session.add(user)
        self.db.session.commit()

        return user

    def get(self, user_id: int | None = None, email: str | None = None) -> User | None:
        if user_id:
            return self.db.session.query(User).filter(User.id == user_id).first()
        elif email:
            return self.db.session.query(User).filter(User.email == email).first()
        else:
            raise ValueError("user_id or email must be provided")

    def update(
        self, user_db: User, user_data: UserDto, survey: SurveyCreate | None = None
    ):
        user_db.email = user_data.email
        user_db.first_name = user_data.first_name
        user_db.last_name = user_data.last_name
        user_db.internal_role = user_data.internal_role
        user_db.level = user_data.level
        user_db.tg_username = user_data.tg_username

        skills: list[Skill] = []
        for skill in user_data.skills:
            skill_db = (
                self.db.session.query(Skill)
                .filter(Skill.skill_name == skill.skill_name)
                .first()
            )
            if skill_db is None:
                skill_db = Skill(**skill.model_dump())
                skills.append(skill_db)

        if len(skills):
            self.db.session.add_all(skills)

        user_db.skills = skills

        if survey:
            roles: list[Role] = []
            for role in survey.roles:
                role_db = (
                    self.db.session.query(Role)
                    .filter(Role.role_name == role.role_name)
                    .first()
                )
                if role_db is None:
                    role_db = Role(**role.model_dump())
                    roles.append(role_db)

            if len(roles):
                self.db.session.add_all(roles)
            user_db.roles = roles

            goals: list[TeamGoal] = []
            for goal in survey.goals:
                goal_db = (
                    self.db.session.query(TeamGoal)
                    .filter(TeamGoal.goal_name == goal.goal_name)
                    .first()
                )
                if goal_db is None:
                    goal_db = TeamGoal(**goal.model_dump())
                    goals.append(goal_db)

            if len(goals):
                self.db.session.add_all(goals)
            user_db.goals = goals

            self.logger.debug(roles)
            self.logger.debug(goals)

        self.db.session.add(user_db)
        self.db.session.commit()

    def delete(self, user_id: int | None = None, email: str | None = None):
        if user_id:
            self.db.session.query(User).filter(User.id == user_id).delete()
        elif email:
            self.db.session.query(User).filter(User.email == email).delete()
        else:
            raise ValueError("user_id or email must be provided")
        self.db.session.commit()

    def get_all(self) -> list[User]:
        return self.db.session.query(User).all()
