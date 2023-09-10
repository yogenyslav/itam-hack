import json
from src.auth.domain import Signup
from src.user.repository import UserRepository
from src.tags.repository import TagsRepository
from src.tags.domain import SkillCreate, TeamGoalCreate, RoleCreate
from src.hackathon.model import team_roles
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.auth.jwt import get_password_hash


db = SQLManager(get_logger("uploader"), local=True)


def upload_users():
    user_repository = UserRepository(db)
    with open("upload/users.json", "r") as f:
        users = json.load(f)

        for user in users:
            try:
                signup = Signup(**user)
                signup.password = get_password_hash(signup.password)
                user_repository.add(signup)
                print(f"uploaded user: {user['email']}")
            except Exception as e:
                print(f"failed to upload role: {user}")


def upload_skills():
    tags_repository = TagsRepository(db)
    with open("upload/skills.json", "r") as f:
        skills = json.load(f)
        for skill in skills:
            try:
                skill_create = SkillCreate(**skill)
                tags_repository.add(skills_data=[skill_create])
                print(f"uploaded skill: {skill}")
            except Exception as e:
                print(f"failed to upload role: {skill}")


def upload_goals():
    tags_repository = TagsRepository(db)
    with open("upload/goals.json", "r") as f:
        goals = json.load(f)
        for goal in goals:
            try:
                goal_create = TeamGoalCreate(**goal)
                tags_repository.add(goals_data=[goal_create])
                print(f"uploaded goal: {goal}")
            except Exception as e:
                print(f"failed to upload role: {goal}")


def upload_roles():
    tags_repository = TagsRepository(db)
    with open("upload/roles.json", "r") as f:
        roles = json.load(f)
        for role in roles:
            try:
                role_create = RoleCreate(**role)
                tags_repository.add(roles_data=[role_create])
                print(f"uploaded role: {role}")
            except Exception as e:
                print(str(e))
                print(f"failed to upload role: {role}")


def upload():
    upload_users()
    upload_skills()
    upload_goals()
    upload_roles()


if __name__ == "__main__":
    upload()
