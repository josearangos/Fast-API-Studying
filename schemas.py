from typing import List, Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

"""
El orm_mode de Pydantic le dirá al modelo 
de Pydantic que lea los datos incluso si no es un dict
sino un modelo ORM (o cualquier otro objeto arbitrario con atributos).

esto nos permite

id = data["id"]

y

id = data.id

Pydantic es compatible con ORM con orm_mode = True
Podrá devolver un modelo de base de datos y leerá los datos de él.
"""

class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True

