from sqlalchemy import Column, Integer, String, Text, Numeric
from sqlalchemy.orm import relationship
from database import Base

class License(Base):
    __tablename__ = 'licenses'

    license_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price_multiplier = Column(Numeric(5,2), default=1.0)

    cart_items = relationship("CartItem", back_populates="license", cascade="all, delete")
    order_items = relationship("OrderItem", back_populates="license", cascade="all, delete")
