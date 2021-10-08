from pydantic import BaseModel
from datetime import datetime


class PictureBase(BaseModel):
    name: str
    content_type: str
    md5: str


class PictureRename(BaseModel):
    id: int
    name: str


class PictureCreate(PictureBase):
    pass


class Picture(PictureBase):
    id: int
    is_active: bool
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True
