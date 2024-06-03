from pydantic import BaseModel


class ProvinsiModel(BaseModel):
    provinsi_id: int
    name_provinsi: str
    ongkir: int


class KabupatenModel(BaseModel):
    kabupaten_id: int
    nama_kabupaten: str


class KecamatanModel(BaseModel):
    kecamatan_id: int
    nama_kecamatan: str


class AlamatResponesModel(BaseModel):
    alamat_id: int
    provinsi: ProvinsiModel
    kabupaten: KabupatenModel
    kecamatan: KecamatanModel

    zip_code: str
    baris_alamat: str


class CreateAlamatModel(BaseModel):
    provinsi_id: int
    kabupaten_id: int
    kecamatan_id: int

    zip_code: str
    baris_alamat: str


class UpdateAlamatModel(BaseModel):
    provinsi_id: int | None = None
    kabupaten_id: int | None = None
    kecamatan_id: int | None = None
    kelurahan_id: int | None = None

    zip_code: str | None = None
    baris_alamat: str | None = None
