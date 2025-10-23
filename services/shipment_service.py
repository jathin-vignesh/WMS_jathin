from sqlalchemy.orm import Session
from models.order_model import Order

def trigger_shipment(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status = "Shipment started"
    db.commit()
    db.refresh(order)
    # Here you could integrate with external shipment APIs or message queues
    return order
