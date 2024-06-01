from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Relationship

from app.database import Base

from .enums import StatusEnum


class Barang(Base):
    __tablename__ = "barang"

    barang_id = Column(Integer, primary_key=True, autoincrement=True)
    kategori_id = Column(Integer, ForeignKey("kategori.kategori_id"))
    nama_barang = Column(String(100), nullable=False)
    deskripsi = Column(Text(), nullable=False)
    file_gambar = Column(String(255), default="21f30ff218f542c581c6ce98cf4c04a0.jpg")
    harga = Column(Integer, default=0, nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default=StatusEnum.ACTIVE)

    dibuat_at = Column(DateTime, default=datetime.now(UTC), server_default=func.now())
    diupdate_at = Column(DateTime, default=datetime.now(UTC), server_default=func.now())

    kategori = Relationship("Kategori", backref="barang")
    list_varian = Relationship(
        "VarianBarang", back_populates="barang", cascade="all, delete-orphan"
    )
