from datetime import datetime
from sqlalchemy import func
from sqlalchemy.engine.row import Row
from src.data.repository import AbstractRepository
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.hackathon.model import Hackathon, HackathonTag, hackathons_to_tags
from src.hackathon.domain import HackathonCreate


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
        hackathon_data: list[HackathonCreate],
    ) -> int:
        hackathons: list[Hackathon] = []
        for hackathon in hackathon_data:
            hackathon_db = Hackathon(**hackathon.model_dump(exclude={"tags"}))
            for tag in hackathon.tags:
                hackathon_db.tags.append(HackathonTag(**tag.model_dump()))
            hackathons.append(hackathon_db)

        self.db.session.add_all(hackathons)
        self.db.session.commit()

        return len(hackathons)

    def get(self, hackathon_id: int | None = None) -> Hackathon | None:
        if hackathon_id:
            return (
                self.db.session.query(Hackathon)
                .filter(Hackathon.id == hackathon_id)
                .first()
            )
        else:
            raise ValueError("hackathon_id must be provided")

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
