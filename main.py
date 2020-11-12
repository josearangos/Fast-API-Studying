from crud import get_users
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from pydantic.fields import Schema
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency
"""
Crea una sesion por solicitud luego de que se resuelve se cierra

Nuestra dependencia creará un nuevo SQLAlchemy SessionLocal que se usará en una sola solicitud
 y luego lo cerrará una vez que finalice la solicitud.

"""
def get_db():
    db = SessionLocal()
    """
    De esta manera nos aseguramos de que la sesión de la base de datos siempre se cierre después de la solicitud. 
    Incluso si hubo una excepción al procesar la solicitud.
    """
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"Hello":"World!!"}


@app.post("/users/",response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.get_user(user)

    if(db_user):
        raise HTTPException(status_code= 400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/",response_model=List[schemas.User])
def read_users(skip: int = 0 , limit: int = 100, db:Session = Depends(get_db)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users

@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db,user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail = "User not found")
    return db_user


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 10, limit: int = 100 , db: Session = Depends(get_db)):
    items = crud.get_items(db,skip=skip, limit=limit)
    return items


""" 
Notes

Alembic: Alembic para "migraciones

Una "migración" es el conjunto de pasos necesarios cada vez 
que cambia la estructura de sus modelos SQLAlchemy, agrega un nuevo atributo, etc. 
para replicar esos cambios en la base de datos, agrega una nueva columna, una nueva tabla, etc.

"""
