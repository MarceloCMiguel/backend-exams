from sqlalchemy.orm import Session
from src.schema.note import NoteCreate, NoteUpdate
from src.model.note import Note
from typing import Dict, List
from src.crud.utils import ExistenceException, NonExistenceException
from fastapi.encoders import jsonable_encoder
from src.crud.subject import get_subject_by_name
# ==================================================================
# Alteracoes Fuziy e Tavernas
'''

- get_all_notes
- create_note
- delete_note
- update_note

PRECISAM DE TESTE

'''
# ==================================================================

def get_all_notes(db: Session) -> List[Note]:
  obj_in_data: List[Note] = db.query(Note).all()
  return obj_in_data

# Talvez precisa do tipo CreateNote dependendo da obrigatoriedade da coluna
def create_note(db: Session, note_in: NoteCreate) -> Note:
  try:
    subject_exist = get_subject_by_name(db,note_in.subject_name)
  except NonExistenceException as err:
    raise err
  db_obj = Note(note=note_in.note,subject_name=note_in.subject_name)
  print(db_obj)
  db.add(db_obj)
  db.commit()
  db.refresh(db_obj)
  return db_obj

def delete_note_by_id(db: Session, note_id: int) -> Note:
  obj_in_data: Note = db.query(Note).filter(Note.id == note_id).first()
  if obj_in_data is None:
    raise NonExistenceException(field=str(note_id))
  db.delete(obj_in_data)
  db.commit()
  return obj_in_data

def update_note_by_id(db: Session, note_id: int, note_in: NoteUpdate) -> Note:
    obj_in_data: Note = db.query(Note).filter(Note.id == note_id).first()
    if obj_in_data is None:
        raise NonExistenceException(field=note_id)
    
    for var, value in vars(note_in).items():
        setattr(obj_in_data, var, value) if value else None
    try:
        subject_exist = get_subject_by_name(db,note_in.subject_name)
    except NonExistenceException as err:
        raise err

    db.add(obj_in_data)
    db.commit()
    db.refresh(obj_in_data)
    return obj_in_data