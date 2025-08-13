from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Beat(Base):
    __tablename__ = 'beats'

    beat_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10,2), nullable=False)
    bpm = Column(Integer)
    genre = Column(String(50))
    musical_key = Column(String(5))
    file_url = Column(Text, nullable=False)
    cover_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    cart_items = relationship("CartItem", back_populates="beat", cascade="all, delete")
    order_items = relationship("OrderItem", back_populates="beat", cascade="all, delete")
    downloads = relationship("Download", back_populates="beat", cascade="all, delete")
