from fastapi import FastAPI,status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

disciplinas= []

class Disciplina(BaseModel):
    """
    This represents the object stored in the database.
    """
    nome: str
    nome_professor: Optional[str] = None
    anotacoes: str
    
@app.get("/disciplina/")
async def get_disciplina():
    return disciplinas

@app.post("/disciplina/")
async def create_disciplina(item: Disciplina):
    for disciplina in  disciplinas:
        if disciplina.nome == item.nome:
            status_code = status.HTTP_400_BAD_REQUEST
            return {"status_code": status_code,"error":"name already in use"}
    disciplinas.append(item)
    return item


