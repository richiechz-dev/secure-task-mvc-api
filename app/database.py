# Creacion de Motor para concetar con una bd 
# Creacion de la funcion session 

from sqlalchemy  import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

sqlite_filename = "securetask.db"
sqlite_url = f"sqlite:///{sqlite_filename}"

connect_arg = {"check_same_thread": False} # check_same_thread es un argumento específico para SQLite que permite que la conexión a la base de datos se comparta entre diferentes hilos. Esto es necesario en aplicaciones web donde múltiples solicitudes pueden acceder a la base de datos simultáneamente.

class Base(DeclarativeBase): # La clase Base sirve para declarar todos los modelos (tablas de la base de datos basados en Objetos)
    pass


# engine es la instancia que nos permite crear nuestra nuestra connection o gestor de conexiones
engine = create_engine(sqlite_url, connect_arg = connect_arg)
SessionLocal = sessionmaker(bind=engine)    #SessionLocal es un objeto fabrica, pues implementa el patron factory

def get_db():
    db = SessionLocal() #creamos una instancia de la clase SessionLocal, que es un objeto de sesión de SQLAlchemy. Esta instancia se utiliza para interactuar con la base de datos.
    try:
        yield db #yield es una palabra clave en Python que se utiliza para crear generadores. En este caso, get_db es una función generadora que produce una instancia de sesión de base de datos cada vez que se llama. Esto permite que la sesión se utilice en un contexto específico (por ejemplo, durante una solicitud HTTP) y luego se cierre automáticamente después de su uso.
    finally:
        db.close() #Finalmente, se cierra la sesión de base de datos para liberar recursos y evitar conexiones abiertas innecesarias.


