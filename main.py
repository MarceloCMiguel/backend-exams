# ==============================================================
# Project by Marcelo Cesário, André Tavernaro e Antonio Fuziy
# ==============================================================

from os import name
from fastapi import FastAPI,status,HTTPException, APIRouter,Depends

from typing import Optional, List
from pydantic import BaseModel
import uvicorn

from src.model.subject import Subject
from src.crud.utils import ExistenceException, NonExistenceException
from src.schema.subject import SubjectInDB, SubjectName, SubjectOutDB,SubjectCreate,SubjectUpdate
from src.schema.note import NoteInDB, NoteOutDB,NoteCreate,NoteUpdate
from src.database.database import Base, engine,SessionLocal
from src.crud.subject import get_all_subjects,get_all_subjects_name, get_subject_by_name, create_subject,delete_subject_by_name, update_subject_by_name
from src.crud.note import delete_note_by_id, get_all_notes, delete_note_by_id, create_note, update_note_by_id
from sqlalchemy.orm import Session
from src.model.note import Note


Base.metadata.create_all(bind=engine,checkfirst=True)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


subjects= []
notes=[]

@app.get("/")
async def root():
    """
    default root message
    """
    return {"message": "Hello World"}

router_subject = APIRouter()



@router_subject.get("/", response_model=List[SubjectInDB])
async def get_subjects(db: Session = Depends(get_db)):
    """
    Get all the subjects
    """
    subjects = get_all_subjects(db)
    return subjects

@router_subject.get("/{name}",response_model=SubjectInDB)
async def get_subject(name:str,db: Session = Depends(get_db)):
    """
    Get a specific subject indentified by an id
    """
    try:
        get_subject_name = get_subject_by_name(db=db, name=name)
    except NonExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return get_subject_name


@router_subject.get("/get_names/",response_model=List[str])
async def get_subjects_name(db: Session = Depends(get_db)):
    """
    Get all the subjects names
    """
    subjects_name = get_all_subjects_name(db)
    return subjects_name


@router_subject.post("/", response_model=SubjectInDB)
async def create_subjects(item: SubjectCreate,db: Session = Depends(get_db)):
    """
    Create a Subject by passing the name, teacher name (optional) and a description
    """
    try:
        created_subject = create_subject(db=db, subject_in=item)
    except ExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return created_subject

@router_subject.delete("/{name}",response_model=SubjectInDB)
async def delete_subject(name: str,db: Session = Depends(get_db)):
    """
    Delete a subject specifying by an id
    """

    try:
        deleted_subject = delete_subject_by_name(db,name)
    except NonExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return deleted_subject



@router_subject.put("/{name}",response_model=SubjectInDB)
async def update_subject(name:str, item: SubjectUpdate, db: Session = Depends(get_db)):
    """
    Change a subject specifying by an id
    """
    try:
        updated_subject = update_subject_by_name(db,name,item)
    except NonExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return updated_subject

app.include_router(router_subject, prefix="/subjects",tags=["Subjects"])

# notes    
router_Note = APIRouter()


@router_Note.get("/", response_model=List[NoteInDB])
async def get_notes(db: Session = Depends(get_db)):
    '''
    Get all the notes
    '''
    notes = get_all_notes(db)
    return notes

@router_Note.post("/notes/", response_model=NoteInDB)
async def create_notes(item: NoteCreate, db: Session = Depends(get_db)):  
    '''
    Create a Note by passing the subject name and the note itself
    '''
    
    try:
        created_note = create_note(db=db, note_in=item)
    except NonExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return created_note

@router_Note.put("/{id}",response_model=NoteInDB)
async def put_Note(id: int,item: NoteUpdate,db: Session = Depends(get_db)):
    '''
    Change a Note specifying by an id
    '''
    try:
        updated_note = update_note_by_id(db,id,item)
    except NonExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return updated_note

@router_Note.delete("/{id}")
async def delete_Note(id: int,db: Session = Depends(get_db)):
    '''
    Delete a Note specifying by an id
    '''
    try:
        deleted_note = delete_note_by_id(db,id)
    except NonExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return deleted_note

app.include_router(router_Note, prefix="/Note",tags=["Notes"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000) 