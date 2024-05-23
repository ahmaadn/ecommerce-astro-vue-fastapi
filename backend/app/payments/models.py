from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, func
from sqlalchemy.orm import Relationship

from app.database import Base

from .enums import PaymentStatus


class Pembayaran(Base):
    __tablename__ = "pembayaran"

    pembayaran_id = Column(Integer, primary_key=True, autoincrement=True)
    pesanan_id = Column(Integer, ForeignKey("pesanan.pesanan_id"), nullable=False)
    total_dibayar = Column(Integer, nullable=False)
    status_bayar = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)

    dibuat_at = Column(DateTime, default=func.now(), server_default=func.now())
    dibayar_at = Column(DateTime)

    pesanan = Relationship("Pesanan", backref="pembayaran")
