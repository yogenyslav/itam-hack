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
        user_db.level = user_data.level
        user_db.tg_username = user_data.tg_username

        if user_data.internal_role:
            user_db.internal_role = user_data.internal_role
            
        if user_data.image_url:
            user_db.image_url = user_data.image_url

        if user_data.graduation_year:
            user_db.graduation_year = user_data.graduation_year

        if user_data.skills:
            user_db.skills = [
                self.db.session.query(Skill).filter(Skill.id == skill.id).one_or_none()
                for skill in user_data.skills
            ]

        if survey:
            user_db.roles = [
                self.db.session.query(Role).filter(Role.id == role.id).one_or_none()
                for role in survey.roles
            ]
            user_db.goals = [
                self.db.session.query(TeamGoal)
                .filter(TeamGoal.id == goal.id)
                .one_or_none()
                for goal in survey.goals
            ]

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

    def get_all(self, limit, offset) -> list[User]:
        return self.db.session.query(User).offset(offset).limit(limit).all()
