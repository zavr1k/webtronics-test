from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Model

from .schemas import PostRead


class Post(Model):
    __tablename__ = "post"

    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    text: Mapped[str] = mapped_column(String(), nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    create_data: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    update_date: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def to_read_model(self) -> PostRead:
        return PostRead(
            id=self.id,
            author_id=self.author_id,
            text=self.text,
            published=self.published,
            create_data=self.create_data,
            update_date=self.update_date,
        )
