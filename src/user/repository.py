from src.data.repository import AbstractRepository
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.user.model import User
from src.user.domain import UserDto
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

    def update(self, user_db: User, user_data: UserDto):
        user_db.email = user_data.email
        user_db.first_name = user_data.first_name
        user_db.last_name = user_data.last_name
        user_db.internal_role = user_data.internal_role
        user_db.level = user_data.level

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
