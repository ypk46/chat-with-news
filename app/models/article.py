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
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    tags: Mapped[List[str]] = mapped_column(
        ARRAY(String(255)), nullable=False, default=list
    )
    published_at: Mapped[datetime] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, insert_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True, insert_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Article {self.id}: {self.title}>"

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
