from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Relationship

from app.database import Base


class Keranjang(Base):
    __tablename__ = "keranjang"

    keranjang_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    varian_barang_id = Column(Integer, ForeignKey("varian_barang.varian_barang_id"), nullable=False)
    jumlah = Column(Integer, nullable=False, default=0)

    dibuat_at = Column(DateTime, default=func.now(), server_default=func.now())

    user = Relationship("User", backref="keranjang")
    variant_barang = Relationship("VarianBarang", backref="keranjang")
