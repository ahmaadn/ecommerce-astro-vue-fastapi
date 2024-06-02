from typing import Annotated, Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi_pagination import Page, paginate

from app.auth.dependencies import get_current_active_admin
from app.category.models import Kategori
from app.database import DependsDB
from app.orders.order.enums import StatusOrder
from app.orders.order.models import Pesanan
from app.orders.order_detail.models import DetailPesanan
from app.upload import handle_file_upload

from ..product_variants.models import VarianBarang
from .enums import StatusEnum
from .models import Barang
from .schemas import BarangResponeModel, BarangUpdateModel, DetailBarangResponeModel
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
async def get_all_barang(
    db: DependsDB,
    q: StatusEnum | Literal["all"] = "all",
    sort_by: Literal["barang_id", "nama_barang", "harga"] = "nama_barang",
    sort_type: Literal["asc", "desc"] = "asc",
):
    query = db.query(Barang)
    if sort_by and sort_type:
        order_by = getattr(getattr(Barang, sort_by), sort_type)()
        query = query.order_by(order_by)

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
    return {"detail": "Product Telah dibuat"}


@r.get("/{barang_id}", response_model=DetailBarangResponeModel, status_code=status.HTTP_200_OK)
async def get_detail_barang(db: DependsDB, barang_id: int):
    return await get_barang(db, barang_id)


@r.post(
    "/update-image",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_admin)],
)
async def update_image_product(
    db: DependsDB, barang_id: Annotated[int, Form], gambar: Annotated[UploadFile, File]
):
    path_gambar = await handle_file_upload(gambar)
    barang = await get_barang(db, barang_id)
    barang.file_gambar = path_gambar
    db.commit()
    db.refresh(barang)
    return {"detail": "Gambar telah diupdate"}


@r.delete("", status_code=status.HTTP_200_OK, dependencies=[Depends(get_current_active_admin)])
async def delete_barang(db: DependsDB, barang_id: int):
    # Get
    pesanan_detail = (
        db.query(DetailPesanan)
        .join(Pesanan, Pesanan.pesanan_id == DetailPesanan.pesanan_id)
        .join(VarianBarang, DetailPesanan.varian_barang_id == VarianBarang.varian_barang_id)
        .where(VarianBarang.barang_id == Barang.barang_id)
        .filter(Pesanan.status != StatusOrder.COMPLETED)
        .all()
    )
    if pesanan_detail:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "barang tidak dapat dihapus")
    barang = await get_barang(db, barang_id)
    db.delete(barang)
    db.commit()
    return {"detail": "pesanan telah berhasil"}


@r.put("", dependencies=[Depends(get_current_active_admin)])
async def barang_update(db: DependsDB, barang_id: int, new_barang: BarangUpdateModel):
    barang_db = await get_barang(db, barang_id)

    for field, value in new_barang.model_dump(exclude_none=True).items():
        setattr(barang_db, field, value)

    db.commit()
    db.refresh(barang_db)
    return {"detail": "barang berhasil di update"}
