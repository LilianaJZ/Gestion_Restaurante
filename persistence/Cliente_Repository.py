from domain.model.Cliente import Cliente
from persistence.Conexion import Conexion

class Cliente_Repository:
    def _init_(self, conexion: Conexion):
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