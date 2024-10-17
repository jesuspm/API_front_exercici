import mysql.connector

#Aquí hacemos una funcion que de forma resumida lo que conseguimos es pasarle los datos para establecer la conexión con nuestra BDD.
def db_client():
    
    try:
        dbname = "Alumnat"
        user = "root"
        password = "1234"
        host = "127.0.0.1"
        port = "3306"
        collation = "utf8mb4_general_ci"
        
        return mysql.connector.connect(
            host = host,
            port = port,
            user = user,
            password = password,
            database = dbname,
            collation = collation
        ) 
            
    except Exception as e:
            return {"status": -1, "message": f"Error de connexió:{e}" }