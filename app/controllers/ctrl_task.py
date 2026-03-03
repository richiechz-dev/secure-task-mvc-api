from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.utils.auth import get_current_user
from app.views.task_view import TaskCreate, TaskDeleteOut, TaskOut, TaskUpdate

router_task = APIRouter(prefix="/tasks", tags=["tasks"])

# Endpoit para tareas


@router_task.post("/", response_model=TaskOut, status_code=201)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_dictionary = task_in.model_dump()  # Convertimos el objeto TaskCreate a un diccionario para poder usarlo en la creación de la tarea

    task = Task(
        title=task_dictionary["title"],
        description=task_dictionary["description"],
        owner_id=current_user.id,
    )  # Creamos la tarea con el diccionario y asignamos el owner_id al id del usuario actual

    db.add(task)  # Guardamos la tarea en la base de datos
    db.commit()
    db.refresh(
        task
    )  # Refrescamos la tarea para obtener el id generado por la base de datos

    return task  # Devolvemos la tarea creada, que se convertirá automáticamente a JSON gracias a Pydantic


@router_task.get("/", response_model=list[TaskOut])
def get_tasks(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    tasks = db.scalars(
        select(Task).where(Task.owner_id == current_user.id)
    ).all()  # Obtenemos todas las tareas del usuario actual filtrando por owner_id
    return tasks


@router_task.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.scalars(
        select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    ).first()  # Buscamos la tarea por id y verificamos que pertenezca al usuario actual

    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    update_data = task_in.model_dump(
        exclude_unset=True
    )  # Solo los campos enviados por el cliente

    for key, value in update_data.items():
        setattr(task, key, value)  # Actualizamos dinámicamente los campos de la tarea

    db.commit()
    db.refresh(task)

    return task


@router_task.delete("/{task_id}", response_model=TaskDeleteOut)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = db.scalars(
        select(Task).where(Task.id == task_id, Task.owner_id == current_user.id)
    ).first()  # Buscamos la tarea por id y verificamos que pertenezca al usuario actual

    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(task)  # Eliminamos la tarea de la base de datos
    db.commit()

    return TaskDeleteOut(message="Tarea eliminada correctamente", id=task_id)
