from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.addresses.models import *  # noqa: F403
from app.auth.router import router as auth_router
from app.carts.cart.models import *  # noqa: F403
from app.carts.cart_detail.models import *  # noqa: F403
from app.category.models import *  # noqa: F403
from app.category.router import router as category_router
from app.config import get_settings
from app.database import Base, engine
from app.orders.order.models import *  # noqa: F403
from app.orders.order_detail.models import *  # noqa: F403
from app.payments.models import *  # noqa: F403
from app.products.product.models import *  # noqa: F403
from app.products.product.router import router as product_router
from app.products.product_variants.models import *  # noqa: F403
from app.products.product_variants.router import router as varian_router
from app.users.models import *  # noqa: F403
from app.users.router import router as users_router

# Create database
Base.metadata.create_all(bind=engine)

# API AROUTER
API_VERSION = get_settings().API_VERSION
api_router = APIRouter(prefix=get_settings().API_VERSION)

api_router.include_router(users_router)
api_router.include_router(auth_router)
api_router.include_router(category_router)
api_router.include_router(product_router)
api_router.include_router(varian_router)

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
