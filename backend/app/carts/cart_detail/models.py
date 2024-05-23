from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Relationship

from app.database import Base


class DetailKeranjang(Base):
    __tablename__ = "detail_keranjang"

    detai_keranjang_id = Column(Integer, primary_key=True, autoincrement=True)
    keranjang_id = Column(
        Integer,
        ForeignKey("keranjang.keranjang_id"),
        nullable=False,
        unique=True,
    )
    varian_barang_id = Column(Integer, ForeignKey("varian_barang.varian_barang_id"), nullable=False)
    jumlah = Column(Integer, nullable=False, default=0)

    keranjang = Relationship("Keranjang", backref="detail_keranjang")
    variant_barang = Relationship("VarianBarang", backref="detail_keranjang")
