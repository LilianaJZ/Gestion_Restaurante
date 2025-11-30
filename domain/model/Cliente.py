class Cliente:
    def __init__(self, id=None, nombre=None, mail=None, telefono=None, ordenes=None):
        self.__id = id
        self.__nombre = nombre
        self.__mail = mail
        self.__telefono = telefono
        self.__ordenes = ordenes if ordenes is not None else []  # agregación: un cliente tiene muchas órdenes

    @property
    def ordenes(self):
        return self.__ordenes
    @ordenes.setter
    def ordenes(self, value):
        self.__ordenes = value

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def mail(self):
        return self.__mail
    @mail.setter
    def mail(self, value):
        self.__mail = value

    @property
    def telefono(self):
        return self.__telefono
    @telefono.setter
    def telefono(self, value):
        self.__telefono = value


    def agregar_orden(self, orden):
        """Agrega una orden al cliente (relación uno a muchos)"""
        self.__ordenes.append(orden)

    def __str__(self):
        return f"Cliente(id={self.__id}, nombre={self.__nombre}, mail={self.__mail}, telefono={self.__telefono}, ordenes={len(self.__ordenes)})"