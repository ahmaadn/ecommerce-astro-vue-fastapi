from pydantic import BaseModel


class ProductVariantBase(BaseModel):
    ukuran: str
    stok: int


class ProductVariantRespones(ProductVariantBase):
    varian_barang_id: int
