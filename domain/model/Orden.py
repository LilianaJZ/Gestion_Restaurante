class Orden:
    def __init__(self, numero_orden=None, fecha=None, cliente_id=None, cliente_nombre=None,
                 plato=None, cantidad=None, precio_total=None, forma_pago=None, cliente=None):
        self.__numero_orden = numero_orden
        self.__fecha = fecha
        self.__cliente_id = cliente_id
        self.__cliente_nombre = cliente_nombre
        self.__plato = plato
        self.__cantidad = cantidad
        self.__precio_total = precio_total
        self.__forma_pago = forma_pago
        self.__cliente = cliente  # agregación: referencia opcional al objeto Cliente

    # --- Getters y setters ---
    @property
    def cliente(self):
        return self.__cliente
    @cliente.setter
    def cliente(self, value):
        self.__cliente = value

    @property
    def numero_orden(self):
        return self.__numero_orden
    @numero_orden.setter
    def numero_orden(self, value):
        self.__numero_orden = value

    @property
    def fecha(self):
        return self.__fecha
    @fecha.setter
    def fecha(self, value):
        self.__fecha = value

    @property
    def cliente_id(self):
        return self.__cliente_id
    @cliente_id.setter
    def cliente_id(self, value):
        self.__cliente_id = value

    @property
    def cliente_nombre(self):
        return self.__cliente_nombre
    @cliente_nombre.setter
    def cliente_nombre(self, value):
        self.__cliente_nombre = value

    @property
    def plato(self):
        return self.__plato
    @plato.setter
    def plato(self, value):
        self.__plato = value

    @property
    def cantidad(self):
        return self.__cantidad
    @cantidad.setter
    def cantidad(self, value):
        self.__cantidad = value

    @property
    def precio_total(self):
        return self.__precio_total
    @precio_total.setter
    def precio_total(self, value):
        self.__precio_total = value

    @property
    def forma_pago(self):
        return self.__forma_pago
    @forma_pago.setter
    def forma_pago(self, value):
        self.__forma_pago = value

    @staticmethod
    def from_row(row):
        return Orden(
            numero_orden=row[0],
            fecha=row[1],
            cliente_id=row[2],
            cliente_nombre=row[3],
            plato=row[4],
            cantidad=row[5],
            precio_total=row[6],
            forma_pago=row[7]
        )

    def to_row(self):
        return [
            self.__numero_orden,
            self.__fecha,
            self.__cliente_id,
            self.__cliente_nombre,
            self.__plato,
            self.__cantidad,
            self.__precio_total,
            self.__forma_pago
        ]

    def __str__(self):
        return (f"Orden(numero_orden={self.__numero_orden}, fecha={self.__fecha}, "
                f"cliente_id={self.__cliente_id}, cliente_nombre={self.__cliente_nombre}, "
                f"plato={self.__plato}, cantidad={self.__cantidad}, "
                f"precio_total={self.__precio_total}, forma_pago={self.__forma_pago})")
