from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.database import get_db
from app.models.user import User
from app.utils.security import hash_password
from app.views.user_view import UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

# endpoint para registrar un usuario
@router.post("/register", response_model=UserOut, status_code=HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Consulta a la base de datos si el usuario existe por email o username
    existing_user = db.execute(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    ).scalar_one_or_none()  # Devuelve un objeto User o None

    # 2. Verificar si el usuario ya existe, en caso de que si se lanza un error 400
    if existing_user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con este email o con este nombre de usuario",
        )
    # 3. Hashear el password del usuario
    hashed_password_user = hash_password(user.password)

    # Creamos al usuario
    new_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password_user
    )

    # 4. Agregar y despues guardar en la base de datos mediante un commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
