from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Relationship

from app.database import Base

from .enums import PaymentStatus


class Pembayaran(Base):
    __tablename__ = "pembayaran"

    pembayaran_id = Column(String(255), primary_key=True, unique=True)
    pesanan_id = Column(Integer, ForeignKey("pesanan.pesanan_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    total_dibayar = Column(Integer, nullable=False)
    status_bayar = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)

    dibuat_at = Column(DateTime, default=func.now(), server_default=func.now())
    dibayar_at = Column(DateTime)

    pesanan = Relationship("Pesanan", backref="pembayaran")
    user = Relationship("User", backref="pembayaran")
