from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from app.database import Base


class VarianBarang(Base):
    __tablename__ = "varian_barang"

    varian_barang_id = Column(Integer, primary_key=True, autoincrement=True)
    barang_id = Column(Integer, ForeignKey("barang.barang_id"), nullable=False)
    ukuran = Column(String(10), nullable=False)
    stok = Column(Integer, default=0)

    barang = Relationship("Barang", backref="varian_barang")
