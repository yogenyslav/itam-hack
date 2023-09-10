from src.data.sql import SQLManager
from src.data.repository import AbstractRepository
from src.utils.logging import get_logger
from src.stats.model import UserStats, UserStatsGraph, InterestsGraph


class StatsRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = get_logger("StatsRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(StatsRepository, cls).__new__(cls)
        return cls.instance

    def add(
        self,
        stats: UserStats | None = None,
        graph: UserStatsGraph | None = None,
        interests_graphs: list[InterestsGraph] | None = None,
    ):
        if stats:
            self.logger.debug(stats)
            self.db.session.add(stats)
        elif graph:
            self.logger.debug(graph)
            self.db.session.add(graph)
        elif interests_graphs:
            self.logger.debug(interests_graphs)
            self.db.session.add_all(interests_graphs)
        else:
            raise ValueError("stats, graph or interests_graphs must be not None")
        self.db.session.commit()

    def get(
        self, user_id: int, stats: bool = False, graph: bool = False
    ) -> UserStats | None:
        if stats:
            self.logger.debug(stats)
            user_stats_db = (
                self.db.session.query(UserStats).filter_by(user_id=user_id).first()
            )
            if not user_stats_db:
                return None
        elif graph:
            self.logger.debug(graph)
            user_stats_graph_db = (
                self.db.session.query(UserStatsGraph)
                .filter(UserStatsGraph.user_id == user_id)
                .first()
            )
            if not user_stats_graph_db:
                return None
        else:
            raise ValueError("stats or graph must be True")

    def update(self):
        pass

    def delete(self):
        pass

    def get_all(self):
        pass
