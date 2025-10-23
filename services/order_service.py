from sqlalchemy.orm import Session
from models.order_model import Order
from models.order_item_model import OrderItem
from schemas.order_schema import OrderCreate
from models.customer_model import Customer
from models.product_model import Product
from fastapi import HTTPException, status

def create_order(db: Session, order_data: OrderCreate):
    #  Step 1: Validate Customer
    customer = db.query(Customer).filter(Customer.id == order_data.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {order_data.customer_id} not found"
        )

    #  Step 2: Validate Products and Calculate Total
    total = 0
    valid_items = []

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.product_id} not found"
            )
        # Optional: Check stock availability
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Not enough stock for product {product.name}"
            )
        p = item.quantity * product.unit_price
        total += item.quantity * product.unit_price
        valid_items.append((product, item,p))

    #  Step 3: Create Order
    order = Order(customer_id=order_data.customer_id, total_amount=total)
    db.add(order)
    db.commit()
    db.refresh(order)

    #  Step 4: Create Order Items and Update Inventory
    for product, item,p in valid_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=p
        )
        db.add(order_item)

        # Reduce stock in Inventory
        product.quantity -= item.quantity

    db.commit()
    db.refresh(order)
    return order
def list_orders(db: Session):
    return db.query(Order).all()

def update_order_status(db: Session, order_id: int, status: str):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = status
        db.commit()
        db.refresh(order)
    return order
