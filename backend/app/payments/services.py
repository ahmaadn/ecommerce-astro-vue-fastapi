import os

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.users.models import User

from .models import Pembayaran

PATH_DOWNLOAD = "./static/downloads"


async def export_to_xlsx(db: Session):
    query = (
        select(
            Pembayaran.pembayaran_id.label("No Pembayaran"),
            Pembayaran.pesanan_id.label("No Pesanan"),
            User.nama.label("Pembeli"),
            Pembayaran.total_dibayar.label("Total dibayar"),
            Pembayaran.status_bayar.label("Status Bayar"),
            Pembayaran.dibayar_at.label("Dibayar tgl"),
            Pembayaran.dibuat_at.label("Dibuat tgl"),
        )
        .select_from(Pembayaran)
        .join_from(User, Pembayaran, Pembayaran.user_id == User.user_id)
    )

    new_df = pd.read_sql(query, db.bind)
    filename = "autos.xlsx"

    with pd.ExcelWriter(
        os.path.join(PATH_DOWNLOAD, filename),
        engine="xlsxwriter",
        mode="w",
        datetime_format="YYYY-MM-DD HH:MM:SS",
    ) as writer:
        new_df.to_excel(writer, index=False)

    return filename
