from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.auth.authentication import AuthBackend
from starlette.middleware.authentication import AuthenticationMiddleware

# MODELS
from app.users.models import *
from app.addresses.models import *
from app.carts.cart.models import *
from app.carts.cart_detail.models import *
from app.category.models import *
from app.orders.order.models import *
from app.orders.order_detail.models import *
from app.payments.models import *
from app.products.product.models import *
from app.products.product_variants.models import *

# ROUTER
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from app.category.router import router as category_router

# Create database
Base.metadata.create_all(bind=engine)

# API AROUTER
API_VERSION = get_settings().API_VERSION
api_router = APIRouter(prefix=API_VERSION)

api_router.include_router(users_router)
api_router.include_router(auth_router)

# APP
app = FastAPI(
    title=get_settings().PROJECT_NAME,
    openapi_url=f"{API_VERSION}/openapi.json",
)
app.include_router(api_router)

# MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
