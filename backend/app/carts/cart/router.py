from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_active_user, is_user_active
from app.database import DependsDB

from ..cart_detail.models import DetailKeranjang
from ..cart_detail.schemas import DetailKeranjangCreate
from .models import Keranjang

r = APIRouter(prefix="/carts", dependencies=Depends(get_current_active_user))


@r.post("/")
async def create_cart_(db: DependsDB, user: is_user_active, keranjang: list[DetailKeranjangCreate]):
    keranjang_db = db.query(Keranjang).where(Keranjang.user_id == user.user_id).first()

    if not keranjang_db:
        keranjang_db = Keranjang(user_id=user.user_id)
        db.add(keranjang_db)
        db.commit()
        db.refresh(keranjang_db)

    for detail_keranjang in keranjang:
        detail_db = DetailKeranjang(
            keranjang_id=keranjang_db.keranjang_id,
            varian_barang_id=detail_keranjang.varian_barang_id,
            jumlah=detail_keranjang.jumlah,
        )
        db.add(detail_db)
        db.commit()
        db.refresh(detail_db)
