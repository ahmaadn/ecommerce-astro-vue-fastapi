from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import is_user_admin
from app.database import DependsDB

from .schemas import ProductVariantBase, ProductVariantRespones
from .services import (
    create_new_varian,
    get_varian_barang,
    get_varian_barang_by_id,
    is_varian_exists,
)

router = r = APIRouter(prefix="/products", tags=["size", "products"])


@r.get("/{barang_id}/variants", response_model=list[ProductVariantRespones])
async def get_all_product_size(db: DependsDB, barang_id: int):
    return await get_varian_barang_by_id(db, barang_id)


@r.post(
    "/{barang_id}/variants",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(is_user_admin)],
)
async def create_varian_barang(db: DependsDB, barang_id: int, new_varian: ProductVariantBase):
    result = await is_varian_exists(db, barang_id, new_varian.ukuran)
    if result:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "variant already exists")
    await create_new_varian(db, barang_id, new_varian.ukuran, new_varian.stok)
    return {"detail": "Product Stock has been created"}


@r.put(
    "/{barang_id}/variants",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(is_user_admin)],
)
async def update_product_size(db: DependsDB, barang_id: int, new_data: ProductVariantRespones):
    varian_db = await get_varian_barang(db, barang_id, new_data.varian_barang_id)
    if new_data.ukuran and str(varian_db.ukuran) == new_data.ukuran:
        varian_db.stok = new_data.stok  # type: ignore

    elif (
        new_data.ukuran
        and str(varian_db.ukuran) != new_data.ukuran
        and not await is_varian_exists(db, barang_id, new_data.ukuran)
    ):
        varian_db.ukuran = new_data.ukuran  # type: ignore
        varian_db.stok = new_data.stok  # type: ignore
    else:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "variant already exists")
    db.commit()
    db.refresh(varian_db)
    return {"detail": "varian has been updated"}


@router.delete(
    "/{barang_id}/variants",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(is_user_admin)],
)
async def product_stock_delete(db: DependsDB, barang_id: int, varian_id: int):
    varian_db = await get_varian_barang(db, barang_id, varian_id)
    db.delete(varian_db)
    db.commit()
    return {"detail": "size has been removed"}
