from pydantic import BaseModel


class KategoriResponseModel(BaseModel):
    kategori_id: int
    nama_kategori: str
