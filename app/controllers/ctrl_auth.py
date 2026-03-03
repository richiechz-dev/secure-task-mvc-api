
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
) # Son clases pilares de Starlette, que son usadas por el framework FastAPI

from app.database import get_db
from app.models.token import Token
from app.models.user import User
from app.utils.security import ( # Formato automatico con ruff suguiendo las normas de PEP8?
    generate_secure_token,
    hash_password,
    verify_password,
)
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


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.execute(
        select(User).where(User.username == form_data.username)
    ).scalar_one_or_none()  # Al consultar basicamente sqlachemy crear un objeto y lo llena con los atributos que le estamos solicitando
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No autorizado")
        
    true_password = verify_password(
        form_data.password, user.hashed_password
    )  # funcion que verifica y regresa true o false. Le pasamos dos argumentos, la contraseña de formulario que envia el usuario y el hash que tenemos en la bd.
    if not true_password:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No autorizado")

    token_key = generate_secure_token()

    new_token = Token(
        key=token_key,
        user_id=user.id,
    )

    db.add(new_token)
    db.commit()

    return {"access_token": token_key, "token_type": "bearer"}
