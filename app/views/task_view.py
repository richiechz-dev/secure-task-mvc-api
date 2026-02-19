from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Título de la tarea, debe tener entre 3 y 100 caracteres.")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la tarea, opcional y con un máximo de 500 caracteres.")

class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    owner_id: int
    
    class Config:
        from_attributes = True  # Pydantic v2

