from domain.model.Orden import Orden
from persistence.Conexion import Conexion
from datetime import datetime
import csv

class Orden_Repository:
    def __init__(self, conexion: Conexion):
        self.conexion = conexion

    # INSERTAR ORDEN

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

        cursor = self.conexion.connection.cursor()
        cursor.execute(query, values)
        self.conexion.connection.commit()

        orden.numero_orden = cursor.lastrowid
        cursor.close()

        print(f"Orden agregada correctamente. Número de orden generado: {orden.numero_orden}")
        return orden

    # OBTENER ORDEN POR ID
    def obtener_orden_por_id(self, numero_orden):
        query = "SELECT * FROM ordenes WHERE numero_orden = %s"
        result = self.conexion.execute_query(query, (numero_orden,))
        if result:
            return Orden.from_row(result[0])
        return None

    # LISTAR TODAS LAS ÓRDENES
    def listar_ordenes(self):
        query = "SELECT * FROM ordenes"
        result = self.conexion.execute_query(query)
        ordenes = []

        if result:
            for row in result:
                ordenes.append(Orden.from_row(row))

        return ordenes


    # LISTAR ÓRDENES POR CLIENTE
    def listar_ordenes_por_cliente(self, cliente_id):
        query = "SELECT * FROM ordenes WHERE cliente_id = %s"
        result = self.conexion.execute_query(query, (cliente_id,))
        ordenes = []

        if result:
            for row in result:
                ordenes.append(Orden.from_row(row))

        return ordenes

    # ACTUALIZAR ORDEN
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

    # ELIMINAR ORDEN
    def eliminar_orden(self, numero_orden):
        query = "DELETE FROM ordenes WHERE numero_orden=%s"
        self.conexion.execute_query(query, (numero_orden,))
        print("Orden eliminada correctamente.")


    # EXPORTAR CSV DE ÓRDENES

    def exportar_csv_ordenes(self, file_path=None):
        query = """
            SELECT numero_orden, fecha, cliente_id, cliente_nombre, plato,
                   cantidad, precio_total, forma_pago
            FROM ordenes
        """

        result = self.conexion.execute_query(query)

        if not result:
            print("No hay órdenes para exportar.")
            return None

        if file_path is None:
            file_path = f"ordenes_{datetime.now().strftime('%d-%m-%Y')}.csv"

        column_names = [
            "numero_orden", "fecha", "cliente_id", "cliente_nombre",
            "plato", "cantidad", "precio_total", "forma_pago"
        ]

        with open(file_path, mode='w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(column_names)

            for row in result:
                orden = Orden.from_row(row)
                writer.writerow(orden.to_row())

        print(f"Archivo CSV exportado correctamente: {file_path}")
        return file_path


    def importar_csv_ordenes(self, file_path):
        try:
            with open(file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    orden = Orden(
                        numero_orden=None,  # se genera automático
                        fecha=row["fecha"],
                        cliente_id=row["cliente_id"],
                        cliente_nombre=row["cliente_nombre"],
                        plato=row["plato"],
                        cantidad=int(row["cantidad"]),
                        precio_total=float(row["precio_total"]),
                        forma_pago=row["forma_pago"]
                    )
                    self.agregar_orden(orden)

            print(f"Órdenes importadas correctamente desde {file_path}")

        except Exception as e:
            print(f"Error al importar CSV: {e}")
