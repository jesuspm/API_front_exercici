import datetime #importamos el modulo datetime para manipular los campos de fechas y horas de nuestra BDD.

#Aquí importamos los modulos que contienen la logica de acceso a la base de datos y las estructuras de datos de la tabla Alumnes.
import db_alumnes 
import alumnes

from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI,HTTPException
from typing import List
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

#Esto es una instancia de la app FastAPI.
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Esto es la raiz del programa que retorna un Hello World.
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Definición del modelo de datos para un alumno usando Pydantic.
class tablaAlumne(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: int
    Grup: str
    DescAula: str
    
    
#Ruta para obtener el listado de los alumnos.
@app.get("/alumnes/list", response_model=List[tablaAlumne])
def read_alumnes():
     # Este return llama a la funcion de acceso a la base de datos y convierte los resultados a un formato Json
    return alumnes.alumnes_schema(db_alumnes.read())

# # Ruta para obtener un alumno específico por su ID.
# @app.get("/alumne/{IdAlumne}", response_model=dict)
# def read_id(IdAlumne: int):
#     # Ruta para obtener un alumno específico por su ID.# Llama a la función que obtiene el alumno por ID.
#     fetchAlumne = db_alumnes.read_id(IdAlumne)
    
#     if fetchAlumne is not None: #Aquí comprobamos si el alumno fue creado o no
#         return alumnes.alumne_schema(fetchAlumne) # Convierte el alumno a formato parecido a Json.
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")  # Si no se encuentra, lanza una excepción 404.

    
# # Ruta para crear un nuevo alumno.  
# @app.post("/create_alumne/")
# async def create_alumne(data: tablaAlumne):
#     # Asigna los datos del alumno a variables individuales.
#     #IdAlumne = data.IdAlumne
#     IdAula = data.IdAula
#     NomAlumne = data.NomAlumne
#     Cicle = data.Cicle
#     Curs = data.Curs
#     Grup = data.Grup
#     CreatedAt = data.CreatedAt
#     UpdateAt = data.UpdateAt
    
#     # Llama a la función que inserta un nuevo alumno en la base de datos y obtiene su ID.
#     l_alumne_id = db_alumnes.create_alumne(IdAula, NomAlumne, Cicle, Curs, Grup, CreatedAt, UpdateAt)
#     return {
#         "msg": "we got data succesfully",
#         "id film": l_alumne_id,
#         "titol": NomAlumne
#     }

# #Aqui definimos la clase AlumneUpdate donde definiremos los atributos que corresponden a los
# #Datos que queremos actualizar.
# class AlumneUpdate(BaseModel):
#     IdAula: int
#     NomAlumne: str
#     Cicle: str
#     Curs: int
#     Grup: str

# #Aqui tenemos el "Decorador" que indica que esta funcion manejara una funcion PUT en la URL indicada
# #En este path al que le pasaremos como parametro el IdAlumne se extraerá de la URL y lo pasaremos como
# #argumento a la función.
# @app.put("/update_alumne/{IdAlumne}") 
# def update_alumne(IdAlumne: int, alumne_data: AlumneUpdate):
#     # Aquí se llama a la función update_alumne del módulo db_alumnes, que se encarga de actualizar los datos en la base de datos.
#     updated_alumne = db_alumnes.update_alumne(
#         IdAlumne, # Este es el ID del alumno que pasaremos por parametro en el Swagger UI.
#         #El resto son los nuevos valores que actualizaremos del alumno con la ID anterior.
#         alumne_data.IdAula, 
#         alumne_data.NomAlumne, 
#         alumne_data.Cicle, 
#         alumne_data.Curs, 
#         alumne_data.Grup
#     )

#     # Aqui controlamos el update, en el caso de que no se actualize ninguno de los campos ejecutará la Exception.
#     if updated_alumne == 0:
#         raise HTTPException(status_code=404, detail="Alumno no encontrado...")

#     #Si está todo ok saltará este mensaje.
#     return {"message": "Alumno Actualizado Correctamente!"}

# #Creamos el "Decorador" donde le pasaremos por parametro la ID a la URL, en nuestro caso usaremos el 
# #Swagger UI para borrarlo.
# @app.delete("/delete_alumne/{IdAlumne}")
# def delete_alumne(IdAlumne: int):
#     deleted_records = db_alumnes.delete_alumne(IdAlumne)
#     if deleted_records == 0:
#         raise HTTPException(status_code=404, detail="Items to delete not found") 

#     return {"Message": "Alumno Eliminado Correctamente!"}