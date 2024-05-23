from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_active_admin
from app.database import DependsDB

from .models import Kategori
from .schemas import KategoriResponseModel

router = r = APIRouter(prefix="/categories")


@r.get("/", response_model=list[KategoriResponseModel])
def get_all_kategori(db: DependsDB, skip: int = 0, limit: int = 10):
    category_db = db.query(Kategori).offset(skip).limit(limit).all()
    return category_db


@r.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_admin)])
async def create_kategori(db: Session, name: str):
    category_db = db.query(Kategori).where(Kategori.nama_kategori == name).first()
    if category_db:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "category name already exists")
    category_db = Kategori(nama_kategori=name)
    db.add(category_db)
    db.commit()
    db.refresh(category_db)
    return {"detail": "categories have been created"}
