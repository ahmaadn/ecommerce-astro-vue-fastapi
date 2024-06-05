from sqlalchemy.orm import Session

from .models import Keranjang

# async def create_keranjang(db: Session, user_id: int):
#     keranjang_db = Keranjang(user_id=user_id)
#     db.add(keranjang_db)
#     db.commit()
#     db.refresh(keranjang_db)
#     return keranjang_db


async def get_keranjang_user(db: Session, user_id: int, variant_barang_id: int):
    keranjang_db = (
        db.query(Keranjang)
        .where(Keranjang.user_id == user_id, Keranjang.varian_barang_id == variant_barang_id)
        .first()
    )

    return keranjang_db
