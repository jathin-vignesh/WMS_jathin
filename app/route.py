from app.routers import customer_routes, order_routes
from fastapi import APIRouter

router = APIRouter()

router.include_router(customer_routes.router)
router.include_router(order_routes.router)