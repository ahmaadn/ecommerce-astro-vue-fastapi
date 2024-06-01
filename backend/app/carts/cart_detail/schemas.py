from pydantic import BaseModel


class DetailKeranjangCreate(BaseModel):
    varian_barang_id: int
    jumlah: int
