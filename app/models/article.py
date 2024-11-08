# Native imports
from typing import List
from datetime import datetime

# 3rd party imports
from sqlalchemy import String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

# Project imports
from app.config import Base
from app.config.db import get_db


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[List[str]] = mapped_column(
        ARRAY(String(255)), nullable=False, default=list
    )
    link: Mapped[str] = mapped_column(Text, nullable=False)
    published_at: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, insert_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True, insert_default=func.now(), onupdate=func.now()
    )
    feed_name: Mapped[str] = mapped_column(String(255), nullable=False)
    feed_image: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"

    @classmethod
    def get(cls, page: int = 1, per_page: int = 10) -> List["Article"]:
        """
        Get articles.

        Args:
            page (int): Page number.
            per_page (int): Number of articles per page.

        Returns:
            list: List of articles.
        """
        db = next(get_db())
        return (
            db.query(cls)
            .order_by(cls.created_at)
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

    @classmethod
    def get_all(cls) -> List["Article"]:
        """
        Get all articles.

         Returns:
            list: List of articles.
        """
        db = next(get_db())
        return db.query(cls).all()

    @classmethod
    def create(cls, data: dict) -> "Article":
        """
        Create a new article.

        Args:
            data (dict): Article data.

        Returns:
            Article: Article instance.
        """
        db = next(get_db())

        try:
            article = cls(**data)
            db.add(article)
            db.commit()
            db.refresh(article)
            return article

        except Exception as e:
            db.rollback()
            raise e

    def to_dict(self):
        """
        Convert article to dictionary.

        Returns:
            dict: Article dictionary.
        """
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "summary": self.summary,
            "tags": self.tags,
            "link": self.link,
            "feed_name": self.feed_name,
            "feed_image": self.feed_image,
            "published_at": self.published_at.isoformat(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
