from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class CartItem(Base):
    __tablename__ = 'cart_items'

    cart_item_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    beat_id = Column(Integer, ForeignKey("beats.beat_id", ondelete="CASCADE"))
    license_id = Column(Integer, ForeignKey("licenses.license_id", ondelete="SET NULL"))
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="cart_items")
    beat = relationship("Beat", back_populates="cart_items")
    license = relationship("License", back_populates="cart_items")
