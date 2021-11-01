from typing import Optional
from pydantic import BaseModel

class Grade(BaseModel):
    """
    This represents the object Grade stored in the database.
    """
    subject_name: str
    grade: int