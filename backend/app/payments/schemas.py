from datetime import datetime

from pydantic import BaseModel

from .enums import PaymentStatus


class PesananModel(BaseModel):
    user_id: int


class PembayaranModel(BaseModel):
    pembayaran_id: str
    pesanan_id: int
    total_dibayar: int
    status_bayar: PaymentStatus
    dibuat_at: datetime
    dibayar_at: datetime

    pesanan: PesananModel
