from sqlalchemy import Boolean, Column, Integer, String, DateTime, func

from .database import Base


class Picture(Base):
    __tablename__ = "pictures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content_type = Column(String)
    md5 = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_valid = Column(Boolean, default=True)
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now())
