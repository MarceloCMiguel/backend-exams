from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text,ForeignKey
from sqlalchemy.orm import relationship

from src.database.database import Base
from src.model.subject import Subject
class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    note= Column(String(80))
    subject_name= Column(String(80), ForeignKey("subjects.name",ondelete='CASCADE',onupdate='CASCADE'),nullable=False)
    subjects = relationship(Subject, primaryjoin=subject_name == Subject.name)
    


