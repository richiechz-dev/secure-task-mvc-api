from pydantic import BaseModel, Field
from pydantic.networks import EmailStr

# Fields agrega metadata y tambien permite agregar restricciones

#Modelo Base o lo que es comun para las demas clases
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario del nuevo usuario, debe tener entre 3 y 50 caracteres.")
    email: EmailStr = Field(..., description="Correo electrónico del nuevo usuario, debe ser una dirección de correo electrónico válida.")

# Modelo de Pydantic para la creación de un nuevo usuario, especificando los campos necesarios para el registro. La receta para validar los datos que entran en la API, asegurando que se cumplan los requisitos de formato y tipo de datos.
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Contraseña del nuevo usuario, debe tener al menos 8 caracteres.")

# Modelo de Pydantic para la salida de datos de un usuario, definiendo los campos que se devolverán al cliente después de realizar operaciones relacionadas con el usuario. Esto ayuda a controlar qué información se expone a través de la API, manteniendo la seguridad y privacidad de los datos del usuario.
class UserOut(UserBase):
    id: int
    is_active: bool
    
    # Importante ya que permite que Pydantic lea los modelos de SQLAlchemy
    # (En Pydantic v2 se usa model_config = {"from_attributes": True})
    class Config:
        from_attributes = True  # Pydantic v2