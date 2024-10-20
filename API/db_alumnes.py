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

def get_aula(desc_aula):
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT IdAula FROM Aula WHERE DescAula = %s", (desc_aula,))
        aula = cur.fetchone()
        return aula  # Devuelve None si no se encuentra, o el IdAula si se encuentra.
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
        
def insert_aula(desc_aula, edifici, pis):
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Aula (DescAula, Edifici, Pis, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())",
            (desc_aula, edifici, pis)
        )
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
        
def get_alumne(nom_alumne, cicle, curs, grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute(
            "SELECT IdAlumne FROM Alumne WHERE NomAlumne = %s AND Cicle = %s AND Curs = %s AND Grup = %s",
            (nom_alumne, cicle, curs, grup)
        )
        alumne = cur.fetchone()
        return alumne  # Devuelve None si no se encuentra, o el IdAlumne si se encuentra.
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
        
        
def insert_alumne(nom_alumne, cicle, curs, grup, desc_aula):
    try:
        conn = db_client()
        cur = conn.cursor()

        # Inserta el alumno en la tabla
        cur.execute("""
            INSERT INTO Alumne (NomAlumne, Cicle, Curs, Grup, DescAula)
            VALUES (%s, %s, %s, %s, %s)
        """, (nom_alumne, cicle, curs, grup, desc_aula))

        # Confirma los cambios
        conn.commit()
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió: {e}"}
    finally:
        conn.close()
