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
from src.schema.subject import SubjectInDB, SubjectOutDB,SubjectCreate,SubjectUpdate
from src.schema.note import NoteInDB, NoteOutDB,NoteCreate,NoteUpdate
from src.database.database import Base, engine,SessionLocal
from src.crud.subject import get_all_subjects, get_subject, create_subject
from src.crud.note import get_all_notes, delete_note, create_note, update_note
from sqlalchemy.orm import Session



Base.metadata.create_all(bind=engine)


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
    # if subjects is None:
    #     raise HTTPException(status_code=404, detail="User not founde")
    # return subjects
@router_subject.get("/{name}")
async def get_subject(name:str):
    """
    Get a specific subject indentified by an id
    """
    for subject in subjects:
        if subject.name == name:
            return subject
    raise HTTPException(status_code=400, detail="Name not found")

@router_subject.get("/get_names/")
async def get_subjects_name():
    """
    Get all the subjects names
    """
    list_names= []
    for subject in subjects:
        list_names.append(subject.name)
    return list_names


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

    subject = create_subject(db,item)
    if subject is None:
        raise HTTPException(status_code=404, detail="User not found")
    return subject

@router_subject.delete("/{name}")
async def delete_subject(name: str):
    """
    Delete a subject specifying by an id
    """
    for subject in subjects:
        if subject.name == name:
            subjects.remove(subject)
            return {"message":f"{subject.name} deleted"}
    raise HTTPException(status_code=400, detail="Name not found")


@router_subject.put("/{name}")
async def update_subject(name:str, item: SubjectUpdate):
    """
    Change a subject specifying by an id
    """
    count = 0
    for subject in subjects:
        if subject.name == name:
            subjects[count] = item
            return  subjects[count]
        count +=1
    raise HTTPException(status_code=400, detail="Name not found")

app.include_router(router_subject, prefix="/subjects",tags=["Subjects"])

# notes    
router_Note = APIRouter()

def check_subject(note: NoteInDB, subjects):
    '''
    check if a subject exist
    '''
    for subject in subjects:
        if subject.name == note.subject_name:
            return True
    return False

def find_last_Note_id(notes):
    '''
    find last id of notes created and return that
    '''
    if len(notes) ==0:
        return 0
    last_Note = notes[-1]
    return last_Note["id"]

# ==================================================================
# Alteracoes Fuziy e Tavernas
'''

- get_notes
- create_notes

PRECISAM DE TESTE

'''
# ==================================================================

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
    except ExistenceException as err:
        raise HTTPException(status_code=400, detail=err.message)
    return created_note
    # if check_subject(item,subjects):
    #     item_ = item.dict()
    #     last_id =find_last_Note_id(notes)
    #     item_["id"] = last_id+1
    #     notes.append(item_)
    #     return item_
    # raise HTTPException(status_code=400, detail="Subject not found")

@router_Note.put("/{id}")
async def put_Note(item: NoteUpdate, id: int):
    '''
    Change a Note specifying by an id
    '''
    count = 0
    for note in notes:
        if note["id"] == id:
            if check_subject(item,subjects):
                item_ = item.dict()
                item_["id"] = id
                notes[count] = item_
                return notes[count]

            raise HTTPException(status_code=400, detail="Subject not found")
        count +=1
    raise HTTPException(status_code=400, detail="Note id not found")

@router_Note.delete("/{id}")
async def delete_Note(id: int):
    '''
    Delete a Note specifying by an id
    '''
    for note in notes:
        if note["id"] == id:
            notes.remove(note)
            return {"message":f"ID {note['id']} deleted"}
    raise HTTPException(status_code=400, detail="Note id not found")

app.include_router(router_Note, prefix="/Note",tags=["Notes"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000) 