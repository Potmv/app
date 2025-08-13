from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    total_amount = Column(Numeric(10,2), nullable=False)
    status = Column(String(20), default='pending')  # pending, paid, canceled
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = 'order_items'

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"))
    beat_id = Column(Integer, ForeignKey("beats.beat_id", ondelete="CASCADE"))
    license_id = Column(Integer, ForeignKey("licenses.license_id", ondelete="SET NULL"))
    quantity = Column(Integer, default=1)
    price = Column(Numeric(10,2), nullable=False)

    order = relationship("Order", back_populates="items")
    beat = relationship("Beat", back_populates="order_items")
    license = relationship("License", back_populates="order_items")
