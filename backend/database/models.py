from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database.base import Base

class Dialog(Base):
    __tablename__ = "dialogs"

    id = Column(String(36), primary_key=True)  # UUID
    title = Column(String(255), nullable=True)  # Название диалога
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Связь с сообщениями
    messages = relationship("Message", back_populates="dialog", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    dialog_id = Column(String(36), ForeignKey("dialogs.id", ondelete="CASCADE"), nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Связь с диалогом
    dialog = relationship("Dialog", back_populates="messages")

class TaskLog(Base):
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(36), index=True)
    status = Column(String(50), nullable=False)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 