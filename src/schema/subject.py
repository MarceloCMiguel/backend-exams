from typing import Optional
from pydantic import BaseModel

class SubjectInDB(BaseModel):
    """
    This represents the object Subject stored in the database.
    """
    name: str
    teacher_name: str
    description: str

    class Config:
        orm_mode = True

        


class SubjectOutDB(BaseModel):
    name: str
    teacher_name: str
    description: str

    class Config:
        orm_mode = True


class SubjectCreate(BaseModel):
    name: str
    description: str
    teacher_name: Optional[str] = ""
    



class SubjectUpdate(BaseModel):
    name: Optional[str]
    teacher_name: Optional[str]
    description: Optional[str]

class SubjectName(BaseModel):
    name: str