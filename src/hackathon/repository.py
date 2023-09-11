from datetime import datetime
from sqlalchemy import func
from sqlalchemy.engine.row import Row
from src.data.repository import AbstractRepository
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.hackathon.model import (
    Hackathon,
    HackathonTag,
    HackathonTeamLfg,
    HackathonTeamLfgEnrollment,
    HackathonTeamLfgInvite,
)
from src.hackathon.domain import (
    HackathonCreate,
    HackathonTeamLfgCreate,
    EnrollmentStatus,
)
from src.user.model import Role, User


class HackathonRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = get_logger("HackathonRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(HackathonRepository, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        hackathon_data: list[HackathonCreate] | None = None,
    ) -> int:
        hackathons: list[Hackathon] = []
        if hackathon_data:

            for hackathon in hackathon_data:
                hackathon_db = Hackathon(**hackathon.model_dump(exclude={"tags"}))
                for tag in hackathon.tags:
                    hackathon_db.tags.append(HackathonTag(**tag.model_dump()))
                hackathons.append(hackathon_db)

            self.db.session.add_all(hackathons)
        self.db.session.commit()

        return len(hackathons)

    def get(
        self,
        hackathon_id: int | None = None,
        team_id: int | None = None,
        enrollment_id: int | None = None,
    ) -> Hackathon | HackathonTeamLfg | None:
        if hackathon_id:
            return (
                self.db.session.query(Hackathon)
                .filter(Hackathon.id == hackathon_id)
                .one_or_none()
            )
        elif team_id:
            return (
                self.db.session.query(HackathonTeamLfg)
                .filter(HackathonTeamLfg.id == team_id)
                .one_or_none()
            )
        elif enrollment_id:
            return (
                self.db.session.query(HackathonTeamLfgEnrollment)
                .filter(HackathonTeamLfgEnrollment.id == enrollment_id)
                .one_or_none()
            )
        else:
            raise ValueError("hackathon_id or team_id must be provided")

    def update(self, hackathon: Hackathon):
        self.db.session.add(hackathon)
        self.db.session.commit()

    def delete(self, hackathon_id: int | None = None):
        if hackathon_id:
            self.db.session.query(Hackathon).filter(
                Hackathon.id == hackathon_id
            ).delete()
        else:
            raise ValueError("hackathon_id must be provided")
        self.db.session.commit()

    def get_all(self, upcoming: bool | None = None) -> list[Hackathon]:
        if upcoming:
            return (
                self.db.session.query(Hackathon)
                .filter(Hackathon.start_date > datetime.now())
                .order_by(Hackathon.start_date)
                .all()
            )
        else:
            return self.db.session.query(Hackathon).all()

    def get_tags(self) -> list[Row[tuple[str, int]]]:
        return (
            self.db.session.query(
                HackathonTag.tag, func.count(HackathonTag.tag).label("count")
            )
            .join(Hackathon.tags)
            .group_by(HackathonTag.tag)
            .all()
        )

    # FIXME: create extra roles
    def add_team_lfg(self, team_data: HackathonTeamLfgCreate, user_id: int):
        user_db = self.db.session.query(User).filter(User.id == user_id).first()

        team = HackathonTeamLfg(**team_data.model_dump(exclude={"required_roles"}))
        team.leader_id = user_id
        team.leader = user_db
        team.members = [user_db]
        team.required_roles = [
            Role(**role.model_dump()) for role in team_data.required_roles
        ]

        self.db.session.add(team)
        self.db.session.commit()
        return team.id

    def get_teams_lfg(
        self, hackathon_id: int | None = None, user_id: int | None = None
    ) -> list[HackathonTeamLfg]:
        if hackathon_id:
            return (
                self.db.session.query(HackathonTeamLfg)
                .filter(HackathonTeamLfg.hackathon_id == hackathon_id)
                .all()
            )
        elif user_id:
            user_db: User = (
                self.db.session.query(User).filter(User.id == user_id).one_or_none()
            )
            if not user_db:
                raise KeyError("user not found")

            return user_db.teams
        return self.db.session.query(HackathonTeamLfg).all()

    def join_team_lfg(self, team_id: int, user_id: int, role_name: str):
        team_enrollment = HackathonTeamLfgEnrollment(
            team_id=team_id, user_id=user_id, role_name=role_name
        )

        user_db = self.db.session.query(User).filter(User.id == user_id).one_or_none()
        if not user_db:
            raise KeyError("user not found")
        user_db.enrollments.append(team_enrollment)

        team_db = (
            self.db.session.query(HackathonTeamLfg)
            .filter(HackathonTeamLfg.id == team_id)
            .one_or_none()
        )
        if team_db:
            team_db.enrollments.append(team_enrollment)

            self.db.session.add(team_enrollment)
            self.db.session.commit()
        else:
            raise KeyError("team not found")

    def get_team_enrollments(
        self,
        enrollment_status: EnrollmentStatus,
        user_id: int | None = None,
        team_id: int | None = None,
        enrollment_id: int | None = None,
    ) -> list[HackathonTeamLfgEnrollment]:
        db_query = self.db.session.query(HackathonTeamLfgEnrollment).filter(
            HackathonTeamLfgEnrollment.status == enrollment_status
        )
        if team_id:
            return db_query.filter(HackathonTeamLfgEnrollment.team_id == team_id).all()
        elif user_id:
            return db_query.filter(HackathonTeamLfgEnrollment.user_id == user_id).all()
        elif enrollment_id:
            return db_query.filter(
                HackathonTeamLfgEnrollment.id == enrollment_id
            ).first()
        else:
            raise ValueError("specify user_id or team_id")

    def accept_team_enrollment(self, enrollment_id: int):
        enrollment_db = (
            self.db.session.query(HackathonTeamLfgEnrollment)
            .filter(HackathonTeamLfgEnrollment.id == enrollment_id)
            .one_or_none()
        )
        if not enrollment_db:
            raise KeyError("enrollment not found accept_team_enrollment")
        enrollment_db.status = EnrollmentStatus.accepted

        team_db: HackathonTeamLfg = enrollment_db.team
        team_db.required_members -= 1
        for role in team_db.required_roles:
            if role.role_name == enrollment_db.role_name:
                team_db.required_roles.remove(role)
                break

        self.db.session.add(enrollment_db)
        self.db.session.add(team_db)

        self.db.session.commit()

    def reject_team_enrollment(self, enrollment_id: int):
        enrollment_db = (
            self.db.session.query(HackathonTeamLfgEnrollment)
            .filter(HackathonTeamLfgEnrollment.id == enrollment_id)
            .one_or_none()
        )
        if not enrollment_db:
            raise KeyError("enrollment not found reject_team_enrollment")

        enrollment_db.status = EnrollmentStatus.denied

        self.db.session.add(enrollment_db)
        self.db.session.commit()

    def add_invite(self, team_id: int, user_id: int):
        invite = HackathonTeamLfgInvite(team_id=team_id, user_id=user_id)
        self.db.session.add(invite)
        self.db.session.commit()

    def get_invites(self, user_id: int) -> list[HackathonTeamLfgInvite]:
        return (
            self.db.session.query(HackathonTeamLfgInvite)
            .filter(HackathonTeamLfgInvite.user_id == user_id)
            .all()
        )

    def accept_invite(self, invite_id: int):
        invite_db = (
            self.db.session.query(HackathonTeamLfgInvite)
            .filter(HackathonTeamLfgInvite.id == invite_id)
            .one_or_none()
        )
        if not invite_db:
            raise KeyError("invite not found accept_invite")
        invite_db.status = EnrollmentStatus.accepted

        team_db = (
            self.db.session.query(HackathonTeamLfg)
            .filter(HackathonTeamLfg.id == invite_db.team_id)
            .one_or_none()
        )
        if not team_db:
            raise KeyError("team not found accept_invite")
        team_db.members.append(invite_db.user)

        self.db.session.delete(invite_db)
        self.db.session.add(team_db)
        self.db.session.commit()

    def reject_invite(self, invite_id: int):
        invite_db = (
            self.db.session.query(HackathonTeamLfgInvite)
            .filter(HackathonTeamLfgInvite.id == invite_id)
            .first()
        )

        self.db.session.delete(invite_db)
        self.db.session.commit()
