from src.data.repository import AbstractRepository
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.hackathon.model import Hackathon, HackathonTag
from src.hackathon.domain import HackathonCreate, HackathonDto, HackathonTagCreate


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

    def get_all(self) -> list[Hackathon]:
        return self.db.session.query(Hackathon).all()
