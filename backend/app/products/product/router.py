from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from fastapi_pagination import Page, paginate

from app.auth.dependencies import get_current_active_admin
from app.category.models import Kategori
from app.database import DependsDB
from app.upload import handle_file_upload

from .enums import StatusEnum
from .models import Barang
from .schemas import BarangResponeModel, DetailBarangResponeModel
from .services import create_barang, get_barang

router = r = APIRouter(
    prefix="/products",
    tags=["product", "products"],
    responses={status.HTTP_404_NOT_FOUND: {"detail": "not found"}},
)


@r.get("", response_model=list[BarangResponeModel], status_code=status.HTTP_200_OK)
async def get_active_barang(db: DependsDB, skip: int = 0, limit: int = 10):
    return (
        db.query(Barang).where(Barang.status == StatusEnum.ACTIVE).offset(skip).limit(limit).all()
    )


@r.get(
    "/all",
    response_model=Page[BarangResponeModel],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_admin)],
)
async def get_all_barang(db: DependsDB, q: StatusEnum | Literal["all"] = "all"):
    query = db.query(Barang)
    if q != "all":
        query = query.where(Barang.status == q)
    return paginate(query.all())


@r.get(
    "/categories/{kategori_id}",
    response_model=list[BarangResponeModel],
    status_code=status.HTTP_200_OK,
)
async def get_barang_by_kategori(db: DependsDB, kategori_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(Barang)
        .join(Kategori)
        .where(Kategori.kategori_id == kategori_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@r.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_active_admin)])
async def barang_create(
    db: DependsDB,
    nama: Annotated[str, Form],
    status: Annotated[StatusEnum, Form],
    deskripsi: Annotated[str, Form],
    kategory_id: Annotated[int | None, Form],
    gambar: Annotated[UploadFile, File],
    harga: Annotated[int, Form],
):
    path_gambar = await handle_file_upload(gambar)
    await create_barang(db, nama, deskripsi, harga, status, path_gambar, kategory_id)
    return {"message": "Product Telah dibuat"}


@r.get("/{barang_id}", response_model=DetailBarangResponeModel, status_code=status.HTTP_200_OK)
async def get_detail_barang(db: DependsDB, barang_id: int):
    return await get_barang(db, barang_id)
