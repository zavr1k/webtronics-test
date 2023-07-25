from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BasePost(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PostCreate(BasePost):
    text: str
    published: bool


class PostRead(BasePost):
    id: int
    author_id: int
    text: str
    published: bool
    create_data: datetime
    update_date: datetime


class PostUpdate(BasePost):
    text: Optional[str] = None
    published: Optional[bool] = None
