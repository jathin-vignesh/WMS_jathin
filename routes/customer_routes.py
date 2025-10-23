from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
from models.customer_model import Customer
from schemas.customer_schema import CustomerCreate, CustomerResponse
from typing import List

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    new_customer = Customer(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer

@router.get("/", response_model=List[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()
