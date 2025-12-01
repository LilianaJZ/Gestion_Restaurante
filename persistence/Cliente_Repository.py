from domain.model.Cliente import Cliente
from persistence.Conexion import Conexion
from datetime import datetime
import csv

class Cliente_Repository:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion

    def agregar_cliente(self, cliente: Cliente):
        query = "INSERT INTO clientes (nombre, mail, telefono) VALUES (%s, %s, %s)"
        values = (cliente.nombre, cliente.mail, cliente.telefono)

        try:
            cursor = self.conexion.connection.cursor()
            cursor.execute(query, values)
            self.conexion.connection.commit()

            cliente.id = cursor.lastrowid
            print("Cliente agregado con éxito. ID generado:", cliente.id)
            cursor.close()
            return cliente

        except Exception as e:
            print("Error al ejecutar la consulta:", e)
            return None

    def obtener_cliente_por_id(self, cliente_id):
        query = "SELECT * FROM clientes WHERE id = %s"
        result = self.conexion.execute_query(query, (cliente_id,))
        if result:
            row = result[0]
            cliente = Cliente(
                id=row[0],
                nombre=row[1],
                mail=row[2],
                telefono=row[3],
                ordenes=[]
            )
            return cliente
        return None

    def listar_clientes(self):
        query = "SELECT * FROM clientes"
        result = self.conexion.execute_query(query)
        clientes = []
        if result:
            for row in result:
                clientes.append(
                    Cliente(id=row[0], nombre=row[1], mail=row[2], telefono=row[3], ordenes=[])
                )
        return clientes

    def actualizar_cliente(self, cliente: Cliente):
        query = """
        UPDATE clientes SET nombre=%s, mail=%s, telefono=%s WHERE id=%s
        """
        values = (cliente.nombre, cliente.mail, cliente.telefono, cliente.id)
        self.conexion.execute_query(query, values)
        print("Cliente actualizado correctamente.")

    def eliminar_cliente(self, cliente_id):
        query = "DELETE FROM clientes WHERE id=%s"
        self.conexion.execute_query(query, (cliente_id,))
        print("Cliente eliminado correctamente.")


    def exportar_csv_clientes(self, file_path=None):
        query = "SELECT id, nombre, mail, telefono FROM clientes"
        result = self.conexion.execute_query(query)

        # Si no hay registros, salimos
        if not result:
            print("No hay registros para exportar.")
            return None

        # Nombre del archivo por defecto
        if file_path is None:
            file_path = f"clientes_{datetime.now().strftime('%d-%m-%Y')}.csv"

        # Nombres de columnas (manual o según tu BD)
        column_names = ["id", "nombre", "mail", "telefono"]

        # Exportar CSV
        with open(file_path, mode='w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)

            for row in result:
                cliente = Cliente.from_row(row)
                writer.writerow(cliente.to_row())

        print(f"Archivo exportado correctamente: {file_path}")
        return file_path

    def importar_csv_clientes(self, file_path="clientes.csv"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    query = """
                        INSERT INTO clientes (id, nombre, mail, telefono)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            nombre = VALUES(nombre),
                            mail = VALUES(mail),
                            telefono = VALUES(telefono)
                    """
                    values = (row["id"], row["nombre"], row["mail"], row["telefono"])

                    # CORRECCIÓN AQUÍ
                    self.conexion.execute_query(query, values)

            print(f"Clientes importados correctamente desde {file_path}.")
        except FileNotFoundError:
            print(f"ERROR: No se encontró el archivo {file_path}.")
