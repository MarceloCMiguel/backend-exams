from typing import Optional
from pydantic import BaseModel

class Subject(BaseModel):
    """
    This represents the object Subject stored in the database.
    """
    name: str
    teacher_name: Optional[str] = None
    description: str