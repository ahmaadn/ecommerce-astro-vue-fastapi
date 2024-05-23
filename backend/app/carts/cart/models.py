from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Relationship

from app.database import Base


class Keranjang(Base):
    __tablename__ = "keranjang"

    keranjang_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), unique=True)

    dibuat_at = Column(DateTime, default=func.now(), server_default=func.now())

    user = Relationship("User", backref="keranjang")
