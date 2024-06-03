from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from app.database import Base


class Kecamatan(Base):
    __tablename__ = "kecamatan"

    kecamatan_id = Column(Integer, primary_key=True, autoincrement=True)
    kabupaten_id = Column(Integer)
    nama_kecamatan = Column(String(100), nullable=False)


class Kabupaten(Base):
    __tablename__ = "kabupaten"

    kabupaten_id = Column(Integer, primary_key=True, autoincrement=True)
    provinsi_id = Column(Integer)
    nama_kabupaten = Column(String(100), nullable=False)


class Provinsi(Base):
    __tablename__ = "provinsi"

    provinsi_id = Column(Integer, primary_key=True, autoincrement=True)
    name_provinsi = Column(String(100), nullable=False)
    ongkir = Column(Integer, default=0)


class Alamat(Base):
    __tablename__ = "alamat"

    alamat_id = Column(Integer, primary_key=True, autoincrement=True)
    provinsi_id = Column(Integer, ForeignKey("provinsi.provinsi_id"), nullable=False)
    kabupaten_id = Column(Integer, ForeignKey("kabupaten.kabupaten_id"), nullable=False)
    kecamatan_id = Column(Integer, ForeignKey("kecamatan.kecamatan_id"), nullable=False)
    zip_code = Column(String(20), nullable=False)
    baris_alamat = Column(String(100), nullable=False)

    user = Relationship("User", back_populates="alamat")
    provinsi = Relationship(Provinsi, backref="alamat")
    kabupaten = Relationship(Kabupaten, backref="alamat")
    kecamatan = Relationship(Kecamatan, backref="alamat")
