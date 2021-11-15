from sqlalchemy.orm import Session
from typing import Dict, List
from src.schema.subject import SubjectInDB, SubjectOutDB, SubjectCreate, SubjectUpdate
from src.model.subject import Subject
from fastapi.encoders import jsonable_encoder
from src.crud.utils import ExistenceException, NonExistenceException

def get_all_subjects(db: Session)->List[Subject]:
    obj_in_data: List[Subject]=db.query(Subject).all()
    return obj_in_data


def get_subject(db: Session, name: str) -> Subject:
    obj_in_data :Subject = db.query(Subject).filter(Subject.name == name).first()
    return obj_in_data

def create_subject(db: Session, subject_in: SubjectCreate) -> Subject:
    """Creates a row with new data in the Subject table
    Args:
        db: a Session instance to execute queries in the database
        subject_on: a SubjectCreate object with the data to be inserted in the table
    Returns:
        The object SubjectModel that was inserted to the table
    Raises:
        HTTPException
    """
    # Transforms object to dict
    obj_in_data: Dict = jsonable_encoder(subject_in)

    # Unpacks dict values to the Subject database model
    db_obj: Subject = Subject(**obj_in_data)

    subject_exists = db.query(Subject).filter(
        Subject.name == db_obj.name).first()

    if subject_exists:
        raise ExistenceException(field=db_obj.name)

    # Inserts the car data to the database
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# ========================================================
# Adicoes do Fuziy e Tavernas
# ========================================================

def delete_subject(db: Session, name: str) -> Subject:
    obj_in_data: Subject = db.query(Subject).filter(Subject.name == name).first()
    if obj_in_data is None:
        raise NonExistenceException(field=name)
    db.delete(obj_in_data)
    db.commit()

    return obj_in_data

def update_subject(db: Session, name: str, subject_in: SubjectUpdate) -> Subject:
    obj_in_data: Subject = db.query(Subject).filter(Subject.name == name).first()
    if obj_in_data is None:
        raise NonExistenceException(field=name)

    obj_data = jsonable_encoder(obj_in_data)
    update_data = subject_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(obj_data, field, update_data[field])

    db.add(obj_data)
    db.commit()
    db.refresh(obj_data)
    return obj_data