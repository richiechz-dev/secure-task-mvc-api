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


