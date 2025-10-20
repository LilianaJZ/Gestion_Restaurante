from domain.model.Orden import Orden
from persistence.Conexion import Conexion

class Orden_Repository:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion

    def agregar_orden(self, orden: Orden):
        query = """
        INSERT INTO ordenes (fecha, cliente_id, cliente_nombre, plato, cantidad, precio_total, forma_pago)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            orden.fecha,
            orden.cliente_id,
            orden.cliente_nombre,
            orden.plato,
            orden.cantidad,
            orden.precio_total,
            orden.forma_pago
        )
        self.conexion.execute_query(query, values)
        print("Orden agregada correctamente.")

    def listar_ordenes_por_cliente(self, cliente_id):
        query = "SELECT * FROM ordenes WHERE cliente_id = %s"
        result = self.conexion.execute_query(query, (cliente_id,))
        ordenes = []
        if result:
            for row in result:
                ordenes.append(
                    Orden(
                        numero_orden=row[0],   # según el orden de las columnas
                        fecha=row[1],
                        cliente_id=row[2],
                        cliente_nombre=row[3],
                        plato=row[4],
                        cantidad=row[5],
                        precio_total=row[6],
                        forma_pago=row[7]
                    )
                )
        return ordenes

    def actualizar_orden(self, orden: Orden):
        query = """
        UPDATE ordenes
        SET fecha=%s, cliente_id=%s, cliente_nombre=%s, plato=%s,
            cantidad=%s, precio_total=%s, forma_pago=%s
        WHERE numero_orden=%s
        """
        values = (
            orden.fecha,
            orden.cliente_id,
            orden.cliente_nombre,
            orden.plato,
            orden.cantidad,
            orden.precio_total,
            orden.forma_pago,
            orden.numero_orden
        )
        self.conexion.execute_query(query, values)
        print("Orden actualizada correctamente.")

    def eliminar_orden(self, numero_orden):
        query = "DELETE FROM ordenes WHERE numero_orden=%s"
        self.conexion.execute_query(query, (numero_orden,))
        print("Orden eliminada correctamente.")
