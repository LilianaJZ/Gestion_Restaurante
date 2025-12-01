import mysql
from mysql import connector


class Conexion:

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

#Metodo de la conexion
    def connect(self):
        try:
            self.connection = mysql.connector.connect(

                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conectado con exito")
        except mysql.connector.Error as error:
            print("No se pudo establecer conexion", error)

#Funcion para desconectar
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexion cerrada.")

#Funcion para ejecutar los queries
    def execute_query(self, query, params=None):
        cursor = self.connection.cursor(buffered=True)
        try:
            cursor.execute(query, params)

            # Detectar si es SELECT (ignorando espacios y saltos de línea)
            if query.strip().lower().startswith("select"):
                result = cursor.fetchall()
                return result

            # Para INSERT, UPDATE, DELETE:
            self.connection.commit()
            return cursor.rowcount  # puede devolver filas afectadas

        except mysql.connector.Error as err:
            print("Error al ejecutar la consulta:", err)
            return None

        finally:
            cursor.close()