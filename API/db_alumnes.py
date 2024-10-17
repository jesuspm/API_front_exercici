from client import db_client

#Creamos una función para sacar un listado de todos los inserts de la tabla Alumne, haciendo previamente una conexión con la bdd y una vez finalizada la tarea cierra la conexión.
def read():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT NomAlumne, Cicle, Curs, Grup, DescAula FROM Alumne JOIN Aula ON Alumne.IdAula = Aula.IdAula;") 
    
        fetchAlumnes = cur.fetchall()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
    
    return fetchAlumnes

