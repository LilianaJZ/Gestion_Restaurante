from domain.model.Orden import Orden
from persistence.Orden_Repository import Orden_Repository
from datetime import datetime


class Orden_Service:
    def __init__(self, orden_repo: Orden_Repository = None):
        self.orden_repo = orden_repo

    def set_repository(self, orden_repo: Orden_Repository):
        """Permite inyectar el repositorio después de inicializar el servicio."""
        self.orden_repo = orden_repo


    # CREAR ORDEN

    def hacer_orden(self, cliente_id, cliente_nombre, plato, cantidad, precio_total, forma_pago):
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        orden = Orden(
            fecha=fecha,
            cliente_id=cliente_id,
            cliente_nombre=cliente_nombre,
            plato=plato,
            cantidad=cantidad,
            precio_total=precio_total,
            forma_pago=forma_pago
        )

        return self.orden_repo.agregar_orden(orden)


    # OBTENER ORDEN POR ID

    def obtener_orden(self, numero_orden):
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        return self.orden_repo.obtener_orden_por_id(numero_orden)


    # ACTUALIZAR ORDEN

    def actualizar_orden(self, numero_orden, **kwargs):
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        orden = self.obtener_orden(numero_orden)
        if not orden:
            raise Exception("Orden no encontrada.")

        # Solo permitimos actualizar campos válidos
        campos_validos = {"fecha", "cliente_id", "cliente_nombre", "plato",
                          "cantidad", "precio_total", "forma_pago"}

        for key, value in kwargs.items():
            if key in campos_validos:
                setattr(orden, key, value)

        self.orden_repo.actualizar_orden(orden)
        return orden


    # ELIMINAR ORDEN

    def eliminar_orden(self, numero_orden):
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        orden = self.obtener_orden(numero_orden)
        if not orden:
            raise Exception("Orden no encontrada.")

        self.orden_repo.eliminar_orden(numero_orden)


    # OBTENER ORDENES DE UN CLIENTE

    def obtener_ordenes_cliente(self, cliente_id):
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        return self.orden_repo.listar_ordenes_por_cliente(cliente_id)


    # EXPORTAR CSV

    def exportar_ordenes_csv(self, file_path=None):
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")
        return self.orden_repo.exportar_csv_ordenes(file_path)

    # IMPORTAR CSV
    def importar_ordenes_csv(self, file_path):
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")
        return self.orden_repo.importar_csv_ordenes(file_path)