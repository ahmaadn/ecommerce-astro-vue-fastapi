from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..product.models import Barang
from ..product.services import get_barang
from .models import VarianBarang


async def get_varian_barang_by_id(db: Session, barang_id: int) -> list[VarianBarang]:
    await get_barang(db, barang_id)
    return db.query(VarianBarang).join(Barang).where(Barang.barang_id == barang_id).all()


async def get_varian_barang(db: Session, barang_id: int, varian_barang_id: int) -> VarianBarang:
    await get_barang(db, barang_id)
    stock_db = (
        db.query(VarianBarang)
        .join(Barang)
        .where(
            VarianBarang.barang_id == barang_id, VarianBarang.varian_barang_id == varian_barang_id
        )
        .first()
    )
    if stock_db is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "product size not found")

    return stock_db


async def is_varian_exists(db: Session, barang_id: int, ukuran: str) -> bool:
    await get_barang(db, barang_id)

    stock_db = (
        db.query(VarianBarang)
        .join(Barang)
        .where(VarianBarang.barang_id == barang_id, VarianBarang.ukuran == ukuran)
        .first()
    )
    return bool(stock_db)


async def create_new_varian(db: Session, barang_id: int, ukuran: str, stok: int):
    varian_db = VarianBarang(barang_id=barang_id, ukuran=ukuran, stok=stok)
    db.add(varian_db)
    db.commit()
    db.refresh(varian_db)
