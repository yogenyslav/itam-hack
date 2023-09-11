from src.data.repository import AbstractRepository
from src.data.sql import SQLManager
from src.utils.logging import get_logger
from src.news.domain import NewsCreate, NewsDto
from src.news.model import News


class NewsRepository(AbstractRepository):
    instance = None

    def __init__(self, db_manager: SQLManager) -> None:
        super().__init__()
        self.db = db_manager
        self.logger = get_logger("NewsRepository")

    def __new__(cls, *args, **kwargs):
        """Singleton pattern"""
        if cls.instance is None:
            cls.instance = super(NewsRepository, cls).__new__(cls)
        return cls.instance

    def add(self, news_data: list[NewsCreate]) -> int:
        news: list[News] = []
        for current_news in news_data:
            news_db = News(**current_news.model_dump())
            news.append(news_db)

        self.db.session.add_all(news)
        self.db.session.commit()
        return len(news)

    def delete(self, news_id: int):
        news = self.db.session.query(News).filter(News.id == news_id).one_or_none()
        if news is None:
            raise KeyError("news not found")
        self.db.session.delete(news)
        self.db.session.commit()

    def update(self, news: News):
        self.db.session.add(news)
        self.db.session.commit()

    def get(self, news_id: int | None = None) -> News | None:
        if news_id:
            return self.db.session.query(News).filter(News.id == news_id).one_or_none()
        else:
            raise ValueError("news_id or title must be specified")

    def get_all(self, offset: int, limit: int) -> list[News]:
        return (
            self.db.session.query(News)
            .order_by(News.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
