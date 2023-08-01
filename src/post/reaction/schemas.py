from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .types import ReactionType


class ReactionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ReactionCreate(ReactionBase):
    reaction: ReactionType


class ReactionRead(ReactionBase):
    id: int
    user_id: int
    post_id: int
    reaction: ReactionType
    create_data: datetime
    update_date: datetime
