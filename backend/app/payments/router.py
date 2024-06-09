from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select

from app.auth.dependencies import get_current_active_user, is_user_active
from app.database import DependsDB
from app.orders.order.models import Pesanan
from app.users.enums import RoleEnum

from .models import Pembayaran
from .schemas import PembayaranModel
from .services import export_to_xlsx

router = r = APIRouter(
    prefix="/payments", tags=["payments"], dependencies=[Depends(get_current_active_user)]
)


@r.get("", status_code=status.HTTP_200_OK, response_model=Page[PembayaranModel])
async def get_history_payment(db: DependsDB, user: is_user_active):
    query = select(Pembayaran).order_by(Pembayaran.dibayar_at)
    if user.role == RoleEnum.USER:
        query = query.join(Pesanan).filter(Pesanan.user_id == user.user_id)

    return paginate(db, query)


@r.get("/export")
async def report_pembayaran(db: DependsDB):
    filename = await export_to_xlsx(db)
    headers = {"Content-Disposition": 'attachment; filename="payment.xlsx"'}
    return FileResponse(f"static/downloads/{filename}", headers=headers)
