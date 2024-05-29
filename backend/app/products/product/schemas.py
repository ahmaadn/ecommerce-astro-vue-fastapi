from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.category.schemas import KategoriResponseModel
from app.config import get_settings
from app.products.product_variants.schemas import ProductVariantRespones

from .enums import StatusEnum


class BarangBaseModel(BaseModel):
    dibuat_at: datetime
    diupdate_at: datetime
    barang_id: int
    nama_barang: str = Field(max_length=100)
    deskripsi: str
    harga: int
    status: StatusEnum


class BarangResponeModel(BarangBaseModel):
    kategori: KategoriResponseModel
    file_gambar: str

    @field_validator("file_gambar", mode="before")
    def src_image(cls, value: str):
        return get_settings().STATIC_MEDIA_URL + "/" + value


class DetailBarangResponeModel(BarangResponeModel):
    list_varian: list[ProductVariantRespones]
