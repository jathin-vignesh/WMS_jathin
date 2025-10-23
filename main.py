from fastapi import FastAPI
from app.routers import customer_routes, order_routes
from db import Base, engine
from models.category_models import Category
from models.product_model import Product
from models.customer_model import Customer
from models.order_item_model import OrderItem
from models.order_model import Order
from app import route

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales & Order Management Service")

app.include_router(route.router)