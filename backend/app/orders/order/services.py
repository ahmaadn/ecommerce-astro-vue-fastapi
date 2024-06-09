import os

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..order_detail.models import DetailPesanan
from .models import Pesanan

PATH_DOWNLOAD = "./static/downloads"


async def export_to_xlsx(db: Session):
    pesanan_df = pd.read_sql(select(Pesanan), db.bind)
    detail_pesanan_df = pd.read_sql(select(DetailPesanan), db.bind)

    # filename = f"payment_{time.time()}.xlsx"
    filename = "orders.xlsx"

    with pd.ExcelWriter(os.path.join(PATH_DOWNLOAD, filename), mode="w") as writer:
        pesanan_df.to_excel(writer, index=False, sheet_name="Pesanan")
        detail_pesanan_df.to_excel(writer, index=False, sheet_name="Detail Pesanan")
    return filename
