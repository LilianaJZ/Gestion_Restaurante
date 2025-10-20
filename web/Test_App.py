import unittest
from persistence.Conexion import Conexion
from persistence.Cliente_Repository import Cliente_Repository
from persistence.Orden_Repository import Orden_Repository
from domain.service.Cliente_Service import Cliente_Service
from domain.service.Orden_Service import Orden_Service

class Test_App(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Se ejecuta una sola vez antes de todas las pruebas"""
        cls.conexion = Conexion(host='localhost', port=3306, user='root', password="", database='restaurante')
        cls.conexion.connect()
        cls.cliente_repo = Cliente_Repository(cls.conexion)
        cls.orden_repo = Orden_Repository(cls.conexion)
        cls.cliente_service = Cliente_Service(cls.cliente_repo)
        cls.orden_service = Orden_Service(cls.orden_repo)

    def test_1_registrar_cliente(self):
        """Prueba que un cliente se registre correctamente"""
        cliente = self.cliente_service.registrar_cliente('Juan Test', 'juan@test.com', '1234567891')
        self.assertIsNotNone(cliente)
        self.assertEqual(cliente.nombre, 'Juan Test')

    def test_2_hacer_orden(self):
        """Prueba que una orden se cree correctamente"""
        # Primero, crear un cliente
        cliente = self.cliente_service.registrar_cliente('Maria Test', 'maria@test.com', '987654321')

        # Luego crear una orden
        orden = self.orden_service.hacer_orden(
            cliente.id, cliente.nombre, 'Pizza Margarita', 2, 50000, 'TC'
        )

        # Validar que la orden fue creada correctamente
        self.assertIsNotNone(orden)
        self.assertEqual(orden.plato, 'Pizza Margarita')
        self.assertEqual(orden.cantidad, 2)
        self.assertEqual(orden.precio_total, 50000)
        self.assertEqual(orden.forma_pago, 'TC')

    @classmethod
    def tearDownClass(cls):
        """Cierra la conexión a la base de datos después de las pruebas"""
        if cls.conexion.connection:
            cls.conexion.connection.close()

if __name__ == "__main__":
    unittest.main()
