from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Relationship

from app.database import Base

from .enums import StatusOrder


class Pesanan(Base):
    __tablename__ = "pesanan"

    pesanan_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    total_harga = Column(Integer, nullable=False)
    ongkir = Column(Integer, default=0)
    status = Column(Enum(StatusOrder), nullable=False, default=StatusOrder.PENDING)

    dibuat_at = Column(DateTime, default=func.now(), server_default=func.now())

    user = Relationship("User", backref="pesanan")
    details_pesanan = Relationship("DetailPesanan", back_populates="pesanan")
