from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.dependencies import get_current_active_user, is_user_active
from app.database import DependsDB
from app.products.product.models import Barang
from app.products.product_variants.models import VarianBarang

from .models import Keranjang
from .schemas import AddToCartModel, CartsResponse, UpdateCartModel
from .services import get_keranjang_user

router = r = APIRouter(
    prefix="/carts", dependencies=[Depends(get_current_active_user)], tags=["carts"]
)


@r.post("")
async def add_to_keranjang(db: DependsDB, user: is_user_active, barang: AddToCartModel):
    keranjang_db = await get_keranjang_user(db, user.user_id, barang.varian_barang_id)

    jumlah = barang.jumlah
    if keranjang_db:
        jumlah += keranjang_db.jumlah

    # cek variant barang apakah tersedia
    variant_barang_db = (
        db.query(VarianBarang)
        .join(Barang)
        .where(
            Barang.barang_id == barang.barang_id,
            VarianBarang.varian_barang_id == barang.varian_barang_id,
        )
        .first()
    )
    if not variant_barang_db:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "variant barang tidak tersedia")

    # Cek stock barang
    if variant_barang_db.stok <= 0:  # type: ignore
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "stock variant barang habis")

    if jumlah <= 0 or jumlah > variant_barang_db.stok:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "melebihi jumlah stok barang")

    if keranjang_db:
        keranjang_db.jumlah = jumlah
    else:
        keranjang_db = Keranjang(
            user_id=user.user_id, varian_barang_id=barang.varian_barang_id, jumlah=jumlah
        )
        db.add(keranjang_db)

    db.commit()
    db.refresh(keranjang_db)

    return {"detail": "barang berhasil ditambahkan ke keranjang"}


@r.get("", status_code=status.HTTP_200_OK, response_model=list[CartsResponse])
async def get_keranjang_details(db: DependsDB, user: is_user_active):
    keranjang_db = db.query(Keranjang).filter(Keranjang.user_id == user.user_id).all()
    # totalHarga = 0

    # for keranjang in keranjang_db:
    #     totalHarga += keranjang.jumlah * keranjang.variant_barang.barang.harga
    #     CartsResponse.model_validate()
    return keranjang_db


@r.put("", status_code=status.HTTP_200_OK)
async def update_detail_keranjang(db: DependsDB, user: is_user_active, cart: UpdateCartModel):
    keranjang_db = (
        db.query(Keranjang)
        .where(Keranjang.keranjang_id == cart.keranjang_id, Keranjang.user_id == user.user_id)
        .first()
    )

    if not keranjang_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Keranjang tidak ditemukan")

    variant_barang_db = (
        db.query(VarianBarang)
        .where(VarianBarang.varian_barang_id == keranjang_db.varian_barang_id)
        .first()
    )

    if cart.jumlah <= 0 or cart.jumlah > variant_barang_db.stok:  # type: ignore
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Melebihi Stok barang")

    keranjang_db.jumlah = cart.jumlah
    db.commit()
    db.refresh(keranjang_db)
    return {"detail": "keranjang berhasil di update"}


@r.delete("", status_code=status.HTTP_200_OK)
async def delete_detail_keranjang(db: DependsDB, user: is_user_active, keranjang_id: int):
    keranjang_db = (
        db.query(Keranjang)
        .where(Keranjang.keranjang_id == keranjang_id, Keranjang.user_id == user.user_id)
        .first()
    )

    if not keranjang_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Keranjang tidak ditemukan")

    db.delete(keranjang_db)
    db.commit()
    return {"detail": "Keranjang berhasil dihapus"}
