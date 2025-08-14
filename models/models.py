from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# -------------------- USER --------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(20), default="customer")  # customer или admin
    created_at = Column(DateTime, default=datetime.utcnow)

    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user", cascade="all, delete")
    downloads = relationship("Download", back_populates="user", cascade="all, delete")
    support_tickets = relationship(
        "SupportTicket", back_populates="user", cascade="all, delete"
    )


# -------------------- LICENSE --------------------
class License(Base):
    __tablename__ = "licenses"

    license_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    price_multiplier = Column(Numeric(5, 2), default=1.0)

    cart_items = relationship(
        "CartItem", back_populates="license", cascade="all, delete"
    )
    order_items = relationship(
        "OrderItem", back_populates="license", cascade="all, delete"
    )


# -------------------- BEAT --------------------
class Beat(Base):
    __tablename__ = "beats"

    beat_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    bpm = Column(Integer)
    genre = Column(String(50))
    musical_key = Column(String(5))
    file_url = Column(Text, nullable=False)
    cover_url = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    cart_items = relationship("CartItem", back_populates="beat", cascade="all, delete")
    order_items = relationship(
        "OrderItem", back_populates="beat", cascade="all, delete"
    )
    downloads = relationship("Download", back_populates="beat", cascade="all, delete")


# -------------------- CART ITEM --------------------
class CartItem(Base):
    __tablename__ = "cart_items"

    cart_item_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    beat_id = Column(Integer, ForeignKey("beats.beat_id", ondelete="CASCADE"))
    license_id = Column(Integer, ForeignKey("licenses.license_id", ondelete="SET NULL"))
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="cart_items")
    beat = relationship("Beat", back_populates="cart_items")
    license = relationship("License", back_populates="cart_items")


# -------------------- ORDER --------------------
class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), default="pending")  # pending, paid, canceled
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"))
    beat_id = Column(Integer, ForeignKey("beats.beat_id", ondelete="CASCADE"))
    license_id = Column(Integer, ForeignKey("licenses.license_id", ondelete="SET NULL"))
    quantity = Column(Integer, default=1)
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    beat = relationship("Beat", back_populates="order_items")
    license = relationship("License", back_populates="order_items")


# -------------------- SUPPORT --------------------
class SupportTicket(Base):
    __tablename__ = "support_tickets"

    ticket_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    subject = Column(String(200), nullable=False)
    status = Column(String(20), default="open")  # open, in_progress, closed
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="support_tickets")
    messages = relationship(
        "SupportMessage", back_populates="ticket", cascade="all, delete"
    )


class SupportMessage(Base):
    __tablename__ = "support_messages"

    message_id = Column(Integer, primary_key=True)
    ticket_id = Column(
        Integer, ForeignKey("support_tickets.ticket_id", ondelete="CASCADE")
    )
    sender_role = Column(String(20), nullable=False)  # customer или admin
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    ticket = relationship("SupportTicket", back_populates="messages")


from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# -------------------- Download --------------------


class Download(Base):
    __tablename__ = "downloads"

    download_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    beat_id = Column(Integer, ForeignKey("beats.beat_id", ondelete="CASCADE"))
    download_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="downloads")
    beat = relationship("Beat", back_populates="downloads")
