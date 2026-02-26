# Modelo token, que representa la tabla "tokens" en la base de datos

from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from datetime import datetime, timedelta, timezone

TOKEN_LIFETIME = timedelta(hours=1) #timedelta es una clase de la biblio datetime que representa una duracion, en nuestro caso de 1 hora, el tiempo que dura el token antes de expirar


class Token(Base):
    __tablename__ = "tokens"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    key : Mapped[str] = mapped_column(String)
    user_id : Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc), 
            nullable=False
        )
    expired_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(timezone.utc) + TOKEN_LIFETIME,
            nullable=False
        )
    
    user = relationship("User", back_populates="tokens")
# default=lambda: datetime.now(timezone.utc) + TOKEN_LIFETIME es una función lambda que se ejecuta cada vez que se crea un nuevo token. Esta función establece el valor predeterminado de expired_at como la fecha y hora actual más la duración del token (TOKEN_LIFETIME). Esto significa que cada token tendrá una fecha de expiración que es exactamente una hora después de su creación.

# datetime.now(timezone.utc) devuelve la fecha y hora actual en formato UTC, es decir, sin tener en cuenta la zona horaria del sistema. Esto es importante para evitar problemas de sincronización entre diferentes zonas horarias.