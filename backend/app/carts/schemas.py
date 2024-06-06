from pydantic import BaseModel

from app.products.product.schemas import BarangResponeModel


class AddToCartModel(BaseModel):
    barang_id: int
    varian_barang_id: int
    jumlah: int


class VariantBarangDetail(BaseModel):
    varian_barang_id: int
    ukuran: str
    stok: int

    barang: BarangResponeModel


class CartsResponse(BaseModel):
    keranjang_id: int
    varian_barang_id: int
    jumlah: int

    variant_barang: VariantBarangDetail


class UpdateCartModel(BaseModel):
    keranjang_id: int
    jumlah: int
