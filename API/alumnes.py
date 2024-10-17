def alumne_schema(tablaAlumne) -> dict:
    return {"NomAlumne": tablaAlumne[0],
            "Cicle": tablaAlumne[1],
            "Curs": tablaAlumne[2],
            "Grup": tablaAlumne[3],
            "DescAula": tablaAlumne[4]
        }

def alumnes_schema(alumnes) -> dict:
    return [alumne_schema(alumne) for alumne in alumnes]