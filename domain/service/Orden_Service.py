from domain.model.Orden import Orden
from persistence.Orden_Repository import Orden_Repository
from datetime import datetime


class Orden_Service:
    def __init__(self, orden_repo: Orden_Repository = None):
        self.orden_repo = orden_repo

    def set_repository(self, orden_repo: Orden_Repository):
        """Permite inyectar el repositorio después de inicializar el servicio"""
        self.orden_repo = orden_repo

    def hacer_orden(self, cliente_id, cliente_nombre, plato, cantidad, precio_total, forma_pago):
        """Crea una nueva orden para un cliente"""
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
        self.orden_repo.agregar_orden(orden)
        return orden

    def obtener_orden(self, cliente_id, numero_orden):
        """Obtiene una orden específica de un cliente"""
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        ordenes = self.orden_repo.listar_ordenes_por_cliente(cliente_id)
        for orden in ordenes:
            if orden.numero_orden == numero_orden:
                return orden
        return None

    def actualizar_orden(self, cliente_id, numero_orden, **kwargs):
        """Actualiza los datos de una orden existente"""
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        orden = self.obtener_orden(cliente_id, numero_orden)
        if not orden:
            raise Exception("Orden no encontrada")

        for key, value in kwargs.items():
            if hasattr(orden, key):
                setattr(orden, key, value)
        self.orden_repo.actualizar_orden(orden)
        return orden

    def eliminar_orden(self, cliente_id, numero_orden):
        """Elimina una orden específica"""
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")

        orden = self.obtener_orden(cliente_id, numero_orden)
        if not orden:
            raise Exception("Orden no encontrada")
        self.orden_repo.eliminar_orden(numero_orden)

    def obtener_ordenes_cliente(self, cliente_id):
        """Devuelve todas las órdenes de un cliente"""
        if not self.orden_repo:
            raise ValueError("Repositorio de órdenes no inicializado.")
        return self.orden_repo.listar_ordenes_por_cliente(cliente_id)
