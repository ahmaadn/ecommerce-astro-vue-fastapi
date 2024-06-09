import os

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Pembayaran

PATH_DOWNLOAD = "./static/downloads"


async def export_to_xlsx(db: Session):
    new_df = pd.read_sql(select(Pembayaran), db.bind)
    # filename = f"payment_{time.time()}.xlsx"
    filename = "autos.xlsx"

    with pd.ExcelWriter(os.path.join(PATH_DOWNLOAD, filename), mode="w") as writer:
        new_df.to_excel(writer, index=False)
    return filename
