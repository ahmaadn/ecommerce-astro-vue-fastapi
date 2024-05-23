from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .enums import StatusEnum
from .models import Barang


async def get_barang(db: Session, barang_id: int):
    barang_db = db.query(Barang).where(Barang.barang_id == barang_id).first()
    if barang_db is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "product not found")
    return barang_db


async def create_barang(
    db: Session,
    nama_barang: str,
    deskripsi: str,
    harga: int,
    status: StatusEnum,
    file_gambar: str,
    kategori_id: int | None = None,
):
    barang_db = Barang(
        nama_barang=nama_barang,
        deskripsi=deskripsi,
        harga=harga,
        status=status,
        file_gambar=file_gambar,
    )
    if kategori_id:
        barang_db.kategori_id = kategori_id

    db.add(barang_db)
    db.commit()
    db.refresh(barang_db)
