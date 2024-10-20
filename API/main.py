from datetime import datetime  # Importamos el módulo datetime para manipular los campos de fechas y horas de nuestra BDD.
import csv  # Importamos el módulo CSV para leer archivos CSV.
from io import StringIO  # Importamos StringIO para manejar el contenido del archivo CSV en memoria.

# Importamos los módulos que contienen la lógica de acceso a la base de datos y las estructuras de datos de la tabla Alumnes.
import db_alumnes 
import alumnes

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
from pydantic import BaseModel

# Instancia de la app FastAPI.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Definición del modelo de datos para un alumno usando Pydantic.
class TablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: str

@app.get("/alumnes/list", response_model=List[TablaAlumne])
def read_alumnes(orderby: str = None, contain: str = None, skip: int = 0, limit: int = None):
    # Obtener la lista de alumnos desde la base de datos
    alumnes_data = db_alumnes.read()  # Este debe devolver una lista de tuplas o listas con los alumnos

    # Filtrar los alumnos si se especifica el parámetro 'contain'
    if contain:
        alumnes_data = [alumne for alumne in alumnes_data if contain.lower() in alumne[0].lower()]

    # Aplicar la ordenación si se especifica 'orderby'
    if orderby == "asc":
        alumnes_data = sorted(alumnes_data, key=lambda x: x[0].lower())
    elif orderby == "desc":
        alumnes_data = sorted(alumnes_data, key=lambda x: x[0].lower(), reverse=True)

    # Aplicar 'skip' y 'limit' para la paginación
    if limit is not None:
        alumnes_data = alumnes_data[skip: skip + limit]
    else:
        alumnes_data = alumnes_data[skip:]

    # Filtrar los campos solicitados
    return [
        {
            "NomAlumne": alumne[0], 
            "Cicle": alumne[1], 
            "Curs": alumne[2], 
            "Grup": alumne[3], 
            "DescAula": alumne[4]
        }
        for alumne in alumnes_data
    ]

@app.post("/alumnes/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):  # Espera un archivo de tipo UploadFile
    # Verificar que el archivo es un CSV
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    # Leer el contenido del archivo CSV
    content = await file.read()
    csv_reader = csv.reader(StringIO(content.decode("utf-8")))

    # Ignorar la cabecera
    header = next(csv_reader)

    # Verificar que la cabecera tenga los campos correctos
    expected_header = ["DescAula", "Edifici", "Pis", "NomAlumne", "Cicle", "Curs", "Grup"]
    if header != expected_header:
        raise HTTPException(status_code=400, detail="Cabecera incorrecta en el archivo CSV")

    # Procesar cada fila del CSV
    for row in csv_reader:
        if len(row) != 7:
            raise HTTPException(status_code=400, detail=f"Formato incorrecto en la fila: {row}")

        # Desestructurar la fila
        desc_aula, edifici, pis, nom_alumne, cicle, curs, grup = row

        # Verificar si el aula ya existe
        if not db_alumnes.get_aula(desc_aula):
            # Si no existe, insertar nueva aula
            db_alumnes.insert_aula(desc_aula, edifici, pis)

        # Verificar si el alumno ya existe
        existing_alumne = db_alumnes.get_alumne(nom_alumne, cicle, curs, grup)
        if existing_alumne:
            continue  # O lanzar una excepción si prefieres no permitir duplicados.

        # Insertar el alumno (sin pasar created_at y updated_at)
        db_alumnes.insert_alumne(nom_alumne, cicle, curs, grup, desc_aula)

    return {"detail": "Càrrega massiva d'alumnes completada correctament"}
