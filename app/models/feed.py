# Native imports
from datetime import datetime

# 3rd party imports
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

# Project imports
from app.config import Base
from app.config.db import get_db


class Feed(Base):
    __tablename__ = "feeds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    image: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )

    @classmethod
    def create(cls, data: dict) -> "Feed":
        """
        Create a new feed.

        Args:
            data (dict): Feed data.

        Returns:
            Feed: Feed instance.
        """
        db = next(get_db())

        try:
            feed = cls(**data)
            db.add(feed)
            db.commit()
            db.refresh(feed)
            return feed

        except Exception as e:
            db.rollback()
            raise e

    @classmethod
    def get_all(cls):
        """
        Get all feeds.

        Returns:
            list: List of feeds.
        """
        db = next(get_db())
        return db.query(cls).all()
