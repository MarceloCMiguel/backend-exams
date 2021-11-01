from os import name
from fastapi import FastAPI,status,HTTPException, APIRouter

from typing import Optional
from pydantic import BaseModel
import uvicorn

from src.schema.subject import Subject
from src.schema.grade import Grade
app = FastAPI()

subjects= []
grades=[]

router_subject = APIRouter()

@app.get("/")
async def root():
    """
    default root message
    """
    return {"message": "Hello World"}

@router_subject.get("/")
async def get_subjects():
    return subjects

@router_subject.get("/{name}")
async def get_subject(name:str):
    for subject in subjects:
        if subject.name == name:
            return subject
    raise HTTPException(status_code=400, detail="Name not found")

@router_subject.get("/get_names/")
async def get_subjects_name():
    list_names= []
    for subject in subjects:
        list_names.append(subject.name)
    return list_names


@router_subject.post("/")
async def create_subjects(item: Subject):
    for subject in  subjects:
        if subject.name == item.name:
            raise HTTPException(status_code=400, detail="Name already in use")

    subjects.append(item)
    return item

@router_subject.delete("/{name}")
async def delete_subject(name: str):
    for subject in subjects:
        if subject.name == name:
            subjects.remove(subject)
            return {"message":f"{subject.name} deleted"}
    raise HTTPException(status_code=400, detail="Name not found")


@router_subject.put("/{name}")
async def update_subject(name:str, item: Subject):
    count = 0
    for subject in subjects:
        if subject.name == name:
            subjects[count] = item
            return  subjects[count]
        count +=1
    raise HTTPException(status_code=400, detail="Name not found")

app.include_router(router_subject, prefix="/subjects",tags=["Subjects"])
# Grades    
router_grade = APIRouter()

def check_subject(grade: Grade, subjects):
    for subject in subjects:
        if subject.name == grade.subject_name:
            return True
    return False

def find_last_grade_id(grades):
    if len(grades) ==0:
        return 0
    last_grade = grades[-1]
    return last_grade["id"]

@router_grade.get("/")
async def get_grades():
    return grades

@router_grade.post("/grades/")
async def create_grades(item: Grade):    
    if check_subject(item,subjects):
        item_ = item.dict()
        last_id =find_last_grade_id(grades)
        item_["id"] = last_id+1
        grades.append(item_)
        return item_
    raise HTTPException(status_code=400, detail="Subject not found")

@router_grade.put("/{id}")
async def put_grade(item: Grade, id: int):
    count = 0
    for grade in grades:
        if grade["id"] == id:
            if check_subject(item,subjects):
                item_ = item.dict()
                item_["id"] = id
                grades[count] = item_
                return grades[count]

            raise HTTPException(status_code=400, detail="Subject not found")
        count +=1
    raise HTTPException(status_code=400, detail="Grade id not found")

@router_grade.delete("/{id}")
async def delete_grade(id: int):
    for grade in grades:
        if grade["id"] == id:
            grades.remove(grade)
            return {"message":f"{grade['id']} deleted"}
    raise HTTPException(status_code=400, detail="Grade id not found")

app.include_router(router_grade, prefix="/grade",tags=["Grades"])







if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000) 