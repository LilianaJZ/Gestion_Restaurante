from persistence.Conexion import Conexion
from persistence.Cliente_Repository import Cliente_Repository
from persistence.Orden_Repository import Orden_Repository
from domain.service.Cliente_Service import Cliente_Service
from domain.service.Orden_Service import Orden_Service
from Menu_App import menu_principal


if __name__ == "__main__":
    # Crear y conectar la base de datos
    conexion = Conexion(host='localhost', port=3306, user='root', password="", database='restaurante')
    conexion.connect()

    # Instanciar repositorios (usan la conexión activa)
    cliente_repo = Cliente_Repository(conexion)
    orden_repo = Orden_Repository(conexion)

    # Instanciar servicios (usan los repositorios)
    cliente_service = Cliente_Service(cliente_repo)
    orden_service = Orden_Service(orden_repo)

    # Ejecutar el menú principal
    menu_principal(cliente_service, orden_service)
