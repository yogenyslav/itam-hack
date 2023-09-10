import json
from src.auth.domain import Signup
from src.user.repository import UserRepository
from src.tags.repository import TagsRepository
from src.tags.domain import SkillCreate, TeamGoalCreate, RoleCreate
from src.stats.model import UserStats, UserStatsGraph, InterestsGraph
from src.stats.domain import StatsCreate, UserStatsGraphCreate, GraphCreate
from src.stats.repository import StatsRepository
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


def upload_stats():
    stats_repository = StatsRepository(db)
    with open("upload/stats.json", "r") as f:
        all_stats = json.load(f)
        for obj in all_stats:
            stats_object = StatsCreate(**obj)
            try:
                stats = UserStats(
                    user_id=stats_object.stats.user_id,
                    days_in_club=stats_object.stats.days_in_club,
                    hack_wins=stats_object.stats.hack_wins,
                    hack_participated=stats_object.stats.hack_participated,
                    messages_in_chats=stats_object.stats.messages_in_chats,
                    avg_responsibility=stats_object.stats.avg_responsibility,
                    avg_communications=stats_object.stats.avg_communications,
                    avg_competence=stats_object.stats.avg_competence,
                    avg_interest=stats_object.stats.avg_interest,
                    avg_leadership=stats_object.stats.avg_leadership,
                )
                stats_graphs = UserStatsGraph(
                    user_id=stats_object.stats_graphs.user_id,
                )
                interests_graphs = stats_graphs.interests_graph

                stats_repository.add(stats=stats)
                stats_repository.add(graph=stats_graphs)
                stats_repository.add(interests_graphs=interests_graphs)
                print(f"uploaded stats: {stats_object}")
            except Exception as e:
                print(str(e))
                print(f"failed to upload stats: {stats_object}")


def upload():
    upload_users()
    upload_skills()
    upload_goals()
    upload_roles()
    # upload_stats()


if __name__ == "__main__":
    upload()
