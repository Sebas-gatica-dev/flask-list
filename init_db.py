# init_db.py
from database import engine, Base

# Crear todas las tablas definidas en los modelos
Base.metadata.create_all(bind=engine)