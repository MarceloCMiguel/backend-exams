from typing import Optional
from pydantic import BaseModel

class Note(BaseModel):
    """
    This represents the object Notes stored in the database.
    """
    subject_name: str
    note: str
