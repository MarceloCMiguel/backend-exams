from os import name
from fastapi import FastAPI,status,HTTPException, APIRouter

from typing import Optional
from pydantic import BaseModel
import uvicorn

from src.schema.subject import Subject
from src.schema.note import Note
app = FastAPI()

subjects= []
notes=[]

@app.get("/")
async def root():
    """
    default root message
    """
    return {"message": "Hello World"}

router_subject = APIRouter()



@router_subject.get("/")
async def get_subjects():
    """
    Get all the subjects
    """
    return subjects

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


@router_subject.post("/")
async def create_subjects(item: Subject):
    """
    Create a Subject by passing the name, teacher name (optional) and a description
    """
    for subject in  subjects:
        if subject.name == item.name:
            raise HTTPException(status_code=400, detail="Name already in use")

    subjects.append(item)
    return item

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
async def update_subject(name:str, item: Subject):
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

def check_subject(note: Note, subjects):
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

@router_Note.get("/")
async def get_notes():
    '''
    Get all the notes
    '''
    return notes

@router_Note.post("/notes/")
async def create_notes(item: Note):  
    '''
    Create a Note by passing the subject name and the note itself
    '''  
    if check_subject(item,subjects):
        item_ = item.dict()
        last_id =find_last_Note_id(notes)
        item_["id"] = last_id+1
        notes.append(item_)
        return item_
    raise HTTPException(status_code=400, detail="Subject not found")

@router_Note.put("/{id}")
async def put_Note(item: Note, id: int):
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