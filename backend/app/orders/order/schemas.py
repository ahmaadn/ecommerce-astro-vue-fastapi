from datetime import datetime

from pydantic import BaseModel

from app.carts.schemas import VariantBarangDetail

from .enums import StatusOrder


class DetailOrderResponese(BaseModel):
    detail_pesanan_id: int
    varian_barang_id: int
    jumlah_pesanan: int
    harga_pesanan: float

    varian_barang: VariantBarangDetail


class PesananRespones(BaseModel):
    pesanan_id: int
    total_harga: int
    status: StatusOrder
    dibuat_at: datetime
    ongkir: int

    details_pesanan: list[DetailOrderResponese]
