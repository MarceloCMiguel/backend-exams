from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text,ForeignKey
from sqlalchemy.orm import relationship

from src.database.database import Base
from src.model.subject import Subject
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    subject_name= Column(String(80), ForeignKey("subject.name"),nullable=False)
    subjects = relationship(Subject, primaryjoin=subject_name == Subject.name)
    note: Column(String(80),nullable=False, index=False)

