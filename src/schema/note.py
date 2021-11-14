from typing import Optional
from pydantic import BaseModel


class NoteInDB(BaseModel):
    """
    This represents the object Notes stored in the database.
    """
    id: int
    subject_name: str
    note: str

    class Config:
        orm_mode = True


class NoteOutDB(BaseModel):
    id: int
    subject_name: str
    note: str



class NoteCreate(BaseModel):
    subject_name: str
    note: str


class NoteUpdate(BaseModel):
    subject_name: Optional[str]
    note: Optional[str]



