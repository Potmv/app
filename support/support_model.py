from sqlalchemy import Column, Integer, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class SupportTicket(Base):
    __tablename__ = 'support_tickets'

    ticket_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    subject = Column(String(200), nullable=False)
    status = Column(String(20), default='open')  # open, in_progress, closed
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="support_tickets")
    messages = relationship("SupportMessage", back_populates="ticket", cascade="all, delete")


class SupportMessage(Base):
    __tablename__ = 'support_messages'

    message_id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey("support_tickets.ticket_id", ondelete="CASCADE"))
    sender_role = Column(String(20), nullable=False)  # customer или admin
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    ticket = relationship("SupportTicket", back_populates="messages")
