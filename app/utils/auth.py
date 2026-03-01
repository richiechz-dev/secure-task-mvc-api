from datetime import datetime, timezone
from app.database import get_db
from app.models.token import Token
from app.models.user import User
from sqlalchemy import select
from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Dependencia para obtener el usuario actual a partir del token Bearer.

    - Verifica que el token exista en la base de datos.
    - Verifica que no haya expirado.
    - Verifica que el usuario asociado exista y esté activo.
    - Si el token está expirado, lo elimina de la BD.
    """
    db_token = db.execute(select(Token).where(Token.key == token)).scalar_one_or_none()
    if not db_token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="No autorizado")

    now = datetime.now(timezone.utc)
    if db_token.expired_at < now:
        # Eliminar token expirado para limpieza
        try:
            db.delete(db_token)
            db.commit()
        except Exception:
            db.rollback()
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token expirado")

    user = db_token.user
    if not user or not user.is_active:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Usuario no autorizado")

    return user