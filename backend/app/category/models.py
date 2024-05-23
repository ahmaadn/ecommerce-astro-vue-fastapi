from sqlalchemy import Column, Integer, String

from app.database import Base


class Kategori(Base):
    __tablename__ = "kategori"
    kategori_id = Column(Integer, primary_key=True, autoincrement=True)
    nama_kategori = Column(String(100), nullable=False)
