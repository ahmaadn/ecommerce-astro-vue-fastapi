from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Relationship

from app.database import Base


class DetailPesanan(Base):
    __tablename__ = "detail_pesanan"

    detail_pesanan_id = Column(Integer, primary_key=True, autoincrement=True)
    pesanan_id = Column(Integer, ForeignKey("pesanan.pesanan_id"), nullable=False)
    varian_barang_id = Column(Integer, ForeignKey("varian_barang.varian_barang_id"), nullable=False)
    jumlah_pesanan = Column(Integer, nullable=False)
    harga_pesanan = Column(DECIMAL(10, 2), nullable=False)

    ditambah_at = Column(DateTime, default=func.now(), server_default=func.now())

    pesanan = Relationship("Pesanan", backref="detail_pesanan")
    varian_barang = Relationship("VarianBarang", backref="detail_pesanan")
