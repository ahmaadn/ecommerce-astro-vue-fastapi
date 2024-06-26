from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_active_admin
from app.database import DependsDB

from .models import Kategori
from .schemas import KategoriResponseModel

router = r = APIRouter(prefix="/categories", tags=["category"])


@r.get("", response_model=list[KategoriResponseModel])
def get_all_kategori(db: DependsDB):
    category_db = db.query(Kategori).all()
    return category_db


@r.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_admin)])
async def create_kategori(db: DependsDB, nama_kategori: str):
    category_db = db.query(Kategori).where(Kategori.nama_kategori == nama_kategori).first()
    if category_db:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "category name already exists")
    category_db = Kategori(nama_kategori=nama_kategori)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return {"detail": "categories have been created"}


@r.put("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_admin)])
async def update_name_kategori(db: DependsDB, kategori_id: int, nama_kategori: str):
    category_db = db.query(Kategori).where(Kategori.kategori_id == kategori_id).first()
    if not category_db:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "kategori tidak ditemukan")

    is_already = (
        db.query(Kategori)
        .where(Kategori.nama_kategori == nama_kategori, Kategori.kategori_id != kategori_id)
        .first()
    )

    if is_already:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "category name already exists")

    category_db.nama_kategori = nama_kategori
    db.commit()
    db.refresh(category_db)
    return {"detail": "kategori berhasil di update"}
