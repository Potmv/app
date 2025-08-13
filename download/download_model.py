from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Download(Base):
    __tablename__ = 'downloads'

    download_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    beat_id = Column(Integer, ForeignKey("beats.beat_id", ondelete="CASCADE"))
    download_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="downloads")
    beat = relationship("Beat", back_populates="downloads")
