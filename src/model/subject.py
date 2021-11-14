from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.database.database import Base

class Subject(Base):
    __tablename__ = "subjects"

    name = Column(String(80), primary_key=True, index=True)
    teacher_name= Column(String(80), nullable=True)
    description= Column(String(180),nullable=True)

