# Modelos sirve para definir las tablas de la base de datos
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# Modelo de Usuario, que representa la tabla "users" en la base de datos
class User(Base):
    __tablename__ = "users"
    
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    username : Mapped[str] = mapped_column(String(30))
    email : Mapped[str] = mapped_column(String(120))
    hashed_password : Mapped[str] = mapped_column(String(120))
    is_active : Mapped[bool] = mapped_column(Boolean, default=True)

# Relaciones: "back_populates" debe coincidir con el nombre en el otro modelo
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    tokens = relationship("Token", back_populates="user", cascade="all, delete-orphan")