from sqlalchemy.orm import Session
from schema.note import NoteCreate, NoteUpdate
from src.model.note import Note
from typing import Dict, List
from src.crud.utils import ExistenceException, NonExistenceException
from fastapi.encoders import jsonable_encoder

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
  obj_in_data: Dict = jsonable_encoder(note_in)

  db_obj = Note(**obj_in_data)
  
  note_exists = db.query(Note).filter(Note.id == db_obj.id).first()

  if note_exists:
    raise ExistenceException(field=str(note_in.id))

  db.add(db_obj)
  db.commit()
  db.refresh(db_obj)
  return db_obj

def delete_note(db: Session, note_id: int) -> Note:
  obj_in_data: Note = db.query(Note).filter(Note.id == note_id).first()
  if obj_in_data is None:
    raise NonExistenceException(field=str(note_id))
  db.delete(obj_in_data)
  db.commit()
  return obj_in_data

def update_note(db: Session, note_id: int, note_in: NoteUpdate) -> Note:
  obj_in_data: Note = db.query(Note).filter(Note.id == note_id).first()
  if obj_in_data is None:
    raise NonExistenceException(field=str(note_id))

  obj_data = jsonable_encoder(note_in)
  update_data = note_in.dict(exclude_unset=True)
  for field in update_data:
    if field in update_data:
      setattr(obj_data, field, update_data[field])

  db.add(obj_data)
  db.commit()
  db.refresh(obj_data)
  return obj_in_data 