from datetime import datetime

from sqlalchemy import (Boolean, DateTime, Enum, ForeignKey, String,
                        UniqueConstraint, func)
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Model

from .schemas import PostRead, ReactionRead
from .types import ReactionType


class Post(Model):
    __tablename__ = "post"

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    text: Mapped[str] = mapped_column(String(), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    create_data: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def to_read_model(self) -> PostRead:
        return PostRead(
            id=self.id,
            author_id=self.author_id,
            text=self.text,
            published=self.published,
            create_data=self.create_data,
            update_date=self.update_date,
        )


class Reaction(Model):
    __tablename__ = "reaction"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    reaction: Mapped[ReactionType] = mapped_column(Enum(ReactionType), nullable=False)
    create_data: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_date: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    def to_read_model(self) -> ReactionRead:
        return ReactionRead(
            id=self.id,
            user_id=self.user_id,
            post_id=self.post_id,
            reaction=self.reaction,
            create_data=self.create_data,
            update_date=self.update_date,
        )
