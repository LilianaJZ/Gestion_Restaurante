from domain.model.Cliente import Cliente
from persistence.Cliente_Repository import Cliente_Repository


class Cliente_Service:
    def __init__(self, cliente_repo: Cliente_Repository):
        self.cliente_repo = cliente_repo

    def crear_cliente(self, nombre, mail, telefono):
        """Crea un nuevo cliente y lo guarda en la base de datos"""
        cliente = Cliente(nombre=nombre, mail=mail, telefono=telefono)
        self.cliente_repo.agregar_cliente(cliente)
        return cliente

    def listar_clientes(self):
        """Devuelve todos los clientes"""
        return self.cliente_repo.listar_clientes()

    def obtener_cliente_por_id(self, cliente_id):
        """Busca un cliente por su ID"""
        return self.cliente_repo.obtener_cliente_por_id(cliente_id)

    def actualizar_cliente(self, id, nombre, mail, telefono):
        """Actualiza los datos de un cliente existente"""
        cliente = Cliente(id=id, nombre=nombre, mail=mail, telefono=telefono)
        self.cliente_repo.actualizar_cliente(cliente)
        return cliente

    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente por su ID"""
        self.cliente_repo.eliminar_cliente(cliente_id)

    def registrar_cliente(self, nombre, mail, telefono):
        cliente = Cliente(nombre=nombre, mail=mail, telefono=telefono)
        self.cliente_repo.agregar_cliente(cliente)
        return cliente

