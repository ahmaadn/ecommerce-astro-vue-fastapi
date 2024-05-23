from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from app.database import Base


class Provinsi(Base):
    __tablename__ = "provinsi"

    provinsi_id = Column(Integer, primary_key=True, autoincrement=True)
    name_provinsi = Column(String(100), nullable=False)
    onkir = Column(Integer, default=0)


class Alamat(Base):
    __tablename__ = "alamat"

    alamat_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    provinsi_id = Column(Integer, ForeignKey("provinsi.provinsi_id"), nullable=False)
    kabupaten = Column(String(100), nullable=False)
    kelurahan = Column(String(100), nullable=False)
    zip_code = Column(String(20), nullable=False)
    baris_alamat = Column(String(100), nullable=False)

    user = Relationship("User", backref="alamat")
    provinsi = Relationship("Provinsi", backref="alamat")
