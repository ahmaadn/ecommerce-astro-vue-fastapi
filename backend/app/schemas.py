from datetime import datetime

from pydantic import BaseModel, Field


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here
    """

    class Config:
        from_attributes = True


class DateTimeModelMixin(BaseModel):
    create_at: datetime = Field(default_factory=datetime.now)
    update_at: datetime = Field(default_factory=datetime.now)


class IDModelMixin(BaseModel):
    id: int
