from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select

from app.addresses.models import Alamat
from app.auth.dependencies import get_current_active_admin, get_current_active_user, is_user_active
from app.carts.models import Keranjang
from app.database import DependsDB
from app.payments.enums import PaymentStatus
from app.payments.models import Pembayaran
from app.products.product_variants.models import VarianBarang
from app.users.enums import RoleEnum

from ..order_detail.models import DetailPesanan
from .enums import StatusOrder
from .models import Pesanan
from .schemas import PesananRespones

router = r = APIRouter(
    prefix="/orders", dependencies=[Depends(get_current_active_user)], tags=["orders"]
)


@r.post("/checkout", status_code=status.HTTP_200_OK)
def checkout(db: DependsDB, user: is_user_active):
    keranjang_all_db = db.query(Keranjang).where(Keranjang.user_id == user.user_id).all()

    if not keranjang_all_db:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Tidak ada barang di keranjang")

    # Membuat pesanan
    pesanan_db = Pesanan(user_id=user.user_id, total_harga=0, status=StatusOrder.PAID)

    # Pesanan detail
    details = []
    total_harga = 0
    for keranjang in keranjang_all_db:
        harga_pesanan = keranjang.jumlah * keranjang.variant_barang.barang.harga
        detail = DetailPesanan(
            pesanan=pesanan_db,
            varian_barang_id=keranjang.varian_barang_id,
            jumlah_pesanan=keranjang.jumlah,
            harga_pesanan=harga_pesanan,
        )

        # variant barang
        varian_db = (
            db.query(VarianBarang)
            .where(VarianBarang.varian_barang_id == keranjang.varian_barang_id)
            .first()
        )

        if varian_db:
            varian_db.stok -= keranjang.jumlah
            db.commit()
            db.refresh(varian_db)

        details.append(detail)
        total_harga += harga_pesanan

    # Orkir
    if user.alamat_id:  # type: ignore
        alamat_db = db.query(Alamat).filter(Alamat.alamat_id == user.alamat_id).first()

        total_harga += alamat_db.provinsi.ongkir  # type: ignore
        pesanan_db.ongkir = alamat_db.provinsi.ongkir

    pesanan_db.total_harga = total_harga

    # Store DB
    db.add(pesanan_db)
    db.add_all(details)
    db.commit()
    db.refresh(pesanan_db)
    [db.refresh(detail) for detail in details]

    # Delete Keranjang
    [db.delete(keranjang) for keranjang in keranjang_all_db]
    db.commit()

    # Pembayaran
    pembayaran_db = Pembayaran(
        pembayaran_id=f"pay-{uuid4().hex}",
        pesanan_id=pesanan_db.pesanan_id,
        total_dibayar=total_harga,
        status_bayar=PaymentStatus.COMPLETED,
        dibayar_at=func.now(),
    )
    db.add(pembayaran_db)
    db.commit()
    db.refresh(pembayaran_db)

    return {"detail": "Berhasil melakukan pembayaran"}


@r.get("", status_code=status.HTTP_200_OK, response_model=Page[PesananRespones])
async def get_order(db: DependsDB, user: is_user_active):
    query = select(Pesanan).order_by(Pesanan.dibuat_at)
    if user.role == RoleEnum.USER:
        query = query.filter(Pesanan.user_id == user.user_id)
    return paginate(db, query)


@r.put(
    "/order/shipped",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_active_admin)],
)
async def shipped(db: DependsDB, pesanan_id: int):
    pesanan_db = db.query(Pesanan).where(Pesanan.pesanan_id == pesanan_id).first()
    if not pesanan_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pesanan tidak ditemukan")

    if pesanan_db.status != StatusOrder.PAID:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, "Pesanan belum dibayar")

    pesanan_db.status = StatusOrder.SHIPPED
    db.commit()
    db.refresh(pesanan_db)
    return {"detail": "pesanan telah dikirim"}


@r.put("/order/completed", status_code=status.HTTP_200_OK)
async def completed_order(db: DependsDB, user: is_user_active, pesanan_id: int):
    pesanan_db = (
        db.query(Pesanan)
        .where(Pesanan.pesanan_id == pesanan_id, Pesanan.user_id == user.user_id)
        .first()
    )

    if not pesanan_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pesanan tidak ditemukan")

    if pesanan_db.status != StatusOrder.SHIPPED:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Pesanan belum terkirim")

    pesanan_db.status = StatusOrder.COMPLETED
    db.commit()
    db.refresh(pesanan_db)
    return {"detail": "Pesanan diselesaikan"}
