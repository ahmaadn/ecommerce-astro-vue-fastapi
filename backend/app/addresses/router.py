from fastapi import APIRouter, HTTPException, status

from app.auth.dependencies import is_user_active
from app.database import DependsDB

from .models import Alamat, Kabupaten, Kecamatan, Provinsi
from .schemas import (
    AlamatResponesModel,
    CreateAlamatModel,
    KabupatenModel,
    KecamatanModel,
    ProvinsiModel,
    UpdateAlamatModel,
)

router = r = APIRouter(prefix="/addresses", tags=["addresses"])


@r.get("", status_code=status.HTTP_200_OK, response_model=AlamatResponesModel)
def get_alamat_user(db: DependsDB, current_user: is_user_active):
    if not current_user.alamat_id:  # type: ignore
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tidak mempunyai alamat")

    alamat_db = db.query(Alamat).filter(Alamat.alamat_id == current_user.alamat_id).first()

    if not alamat_db:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Tidak mempunyai alamat")

    return alamat_db


@r.post("", status_code=status.HTTP_200_OK)
def buat_alamat_user(db: DependsDB, current_user: is_user_active, alamat: CreateAlamatModel):
    alamat_db = db.query(Alamat).filter(Alamat.alamat_id == current_user.alamat_id).first()
    if alamat_db:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Sudah mempunyai alamat")

    alamat_db = Alamat(
        provinsi_id=alamat.provinsi_id,
        kabupaten_id=alamat.kabupaten_id,
        kecamatan_id=alamat.kecamatan_id,
        zip_code=alamat.zip_code,
        baris_alamat=alamat.baris_alamat,
    )
    db.add(alamat_db)
    db.commit()
    db.refresh(alamat_db)
    current_user.alamat = alamat_db
    db.commit()
    db.refresh(current_user)
    return {"detail": "Alamat berhasil dibuat"}


@r.put("", status_code=status.HTTP_200_OK)
def update_alamat_user(db: DependsDB, current_user: is_user_active, alamat: UpdateAlamatModel):
    alamat_db = db.query(Alamat).where(Alamat.alamat_id == current_user.alamat_id).first()
    if not alamat_db:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Buat alamat terlebih dahulu")

    if alamat.provinsi_id:
        provinsi_db = db.query(Provinsi).where(Provinsi.provinsi_id == alamat.provinsi_id).first()
        if not provinsi_db:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Provinsi tidak terdaftar")

    for field, value in alamat.model_dump(exclude_none=True).items():
        setattr(alamat_db, field, value)

    return {"detail": "alamat sudah diupdate"}


@r.get("/provinsi", status_code=status.HTTP_200_OK, response_model=list[ProvinsiModel])
def get_provinsi(db: DependsDB):
    return db.query(Provinsi).order_by(Provinsi.name_provinsi.asc()).all()


@r.get("/kabupaten", status_code=status.HTTP_200_OK, response_model=list[KabupatenModel])
def get_kabupaten(db: DependsDB, provinsi_id: int):
    kabupaten = (
        db.query(Kabupaten)
        .filter(Kabupaten.provinsi_id == provinsi_id)
        .order_by(Kabupaten.nama_kabupaten.asc())
        .all()
    )
    return kabupaten


@r.get("/kecamatan", status_code=status.HTTP_200_OK, response_model=list[KecamatanModel])
def get_kecamatan(db: DependsDB, kabupaten_id: int):
    kecamatan = (
        db.query(Kecamatan)
        .filter(Kecamatan.kabupaten_id == kabupaten_id)
        .order_by(Kecamatan.nama_kecamatan.asc())
        .all()
    )
    return kecamatan
