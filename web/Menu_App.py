from fpdf import FPDF
import os

MENU = [
    {"nombre": "Hamburguesa Clásica", "descripcion": "Carne de res, queso, lechuga y tomate.", "tamano": "Regular", "precio": 12000},
    {"nombre": "Pizza Margarita", "descripcion": "Tomate, mozzarella, albahaca y aceite de oliva.", "tamano": "Mediana", "precio": 25000},
    {"nombre": "Ensalada César", "descripcion": "Lechuga romana, croutons, queso parmesano y aderezo César.", "tamano": "Grande", "precio": 15000}
]

METODOS_PAGO = ["TD", "TC", "Efectivo", "Bono"]


def menu_principal(cliente_service, orden_service):
    def limpiar_pantalla():
        os.system('cls' if os.name == 'nt' else 'clear')

    def imprimir_orden(orden):
        limpiar_pantalla()
        print("=" * 30)
        print("      RECIBO DE ORDEN      ")
        print("=" * 30)
        print(f"Orden No. {str(orden.numero_orden).zfill(3)}")
        print(f"Fecha: {orden.fecha}")
        print(f"Cliente: {orden.cliente_nombre}")
        print("-" * 30)
        print(f"Plato: {orden.plato}")
        print(f"Cantidad: {orden.cantidad}")
        print(f"Forma de Pago: {orden.forma_pago}")
        print("-" * 30)
        print(f"TOTAL: ${orden.precio_total:,}")
        print("=" * 30)
        print("¡Gracias por tu compra!")

        # Crear carpeta si no existe
        if not os.path.exists("recibos"):
            os.makedirs("recibos")

        # Generar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "RECIBO DE ORDEN", ln=True, align="C")
        pdf.cell(0, 10, "=" * 30, ln=True, align="C")
        pdf.cell(0, 10, f"Orden No. {str(orden.numero_orden).zfill(3)}", ln=True)
        pdf.cell(0, 10, f"Fecha: {orden.fecha}", ln=True)
        pdf.cell(0, 10, f"Cliente: {orden.cliente_nombre}", ln=True)
        pdf.cell(0, 10, "-" * 30, ln=True)
        pdf.cell(0, 10, f"Plato: {orden.plato}", ln=True)
        pdf.cell(0, 10, f"Cantidad: {orden.cantidad}", ln=True)
        pdf.cell(0, 10, f"Forma de Pago: {orden.forma_pago}", ln=True)
        pdf.cell(0, 10, "-" * 30, ln=True)
        pdf.cell(0, 10, f"TOTAL: ${orden.precio_total:,}", ln=True)
        pdf.cell(0, 10, "=" * 30, ln=True, align="C")
        pdf.cell(0, 10, "¡Gracias por tu compra!", ln=True, align="C")

        nombre_archivo = f"recibos/recibo_orden_{orden.numero_orden}.pdf"
        pdf.output(nombre_archivo)
        print(f"\nRecibo PDF generado: {nombre_archivo}")

    cliente_actual = None

    while True:
        limpiar_pantalla()
        print("\nSeleccione una opción:")
        print("1. Registrar Cliente")
        print("2. Hacer una Orden")
        print("3. Consultar Menú")
        print("4. Consultar Mis Datos")
        print("5. Consultar Mis Órdenes")
        print("6. Salir")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            limpiar_pantalla()
            print("--- REGISTRAR CLIENTE ---")
            nombre = input("Nombre: ").strip()
            mail = input("Email: ").strip()
            telefono = input("Teléfono: ").strip()

            cliente_actual = cliente_service.registrar_cliente(nombre, mail, telefono)
            print("\nCliente registrado con éxito.")
            input("Presiona Enter para continuar...")

        elif opcion == "2":
            if not cliente_actual:
                print("Primero debe registrar un cliente.")
                input("Presiona Enter para continuar...")
                continue

            limpiar_pantalla()
            print("--- HACER ORDEN ---")
            for i, plato in enumerate(MENU):
                print(f"{i+1}. {plato['nombre']} - ${plato['precio']} - {plato['tamano']}")

            num_plato = input("Seleccione el número del plato: ").strip()
            if not num_plato.isdigit() or int(num_plato) < 1 or int(num_plato) > len(MENU):
                print("Opción inválida.")
                input("Presiona Enter para continuar...")
                continue

            plato_elegido = MENU[int(num_plato) - 1]
            cantidad = input("Cantidad: ").strip()

            if not cantidad.isdigit() or int(cantidad) < 1:
                print("Cantidad inválida.")
                input("Presiona Enter para continuar...")
                continue

            cantidad = int(cantidad)
            print("Formas de pago:")
            for i, metodo in enumerate(METODOS_PAGO):
                print(f"{i+1}. {metodo}")

            num_pago = input("Seleccione el número de forma de pago: ").strip()
            if not num_pago.isdigit() or int(num_pago) < 1 or int(num_pago) > len(METODOS_PAGO):
                print("Opción inválida.")
                input("Presiona Enter para continuar...")
                continue

            forma_pago = METODOS_PAGO[int(num_pago) - 1]
            precio_total = plato_elegido['precio'] * cantidad

            orden = orden_service.hacer_orden(
                cliente_actual.id,
                cliente_actual.nombre,
                plato_elegido['nombre'],
                cantidad,
                precio_total,
                forma_pago
            )

            print(f"\nOrden generada con éxito. Total: ${precio_total:,}")
            imprimir = input("¿Desea imprimir el recibo? (s/n): ").strip().lower()
            if imprimir == "s":
                imprimir_orden(orden)
            input("Presiona Enter para continuar...")

        elif opcion == "3":
            limpiar_pantalla()
            print("--- MENÚ DEL RESTAURANTE ---")
            for plato in MENU:
                print(f"{plato['nombre']} - {plato['descripcion']} - {plato['tamano']} - ${plato['precio']}")
            input("Presiona Enter para continuar...")

        elif opcion == "4":
            limpiar_pantalla()
            if not cliente_actual:
                print("No hay cliente registrado.")
            else:
                print("--- DATOS DEL CLIENTE ---")
                print(f"ID: {cliente_actual.id}")
                print(f"Nombre: {cliente_actual.nombre}")
                print(f"Email: {cliente_actual.mail}")
                print(f"Teléfono: {cliente_actual.telefono}")
            input("Presiona Enter para continuar...")

        elif opcion == "5":
            limpiar_pantalla()
            if not cliente_actual:
                print("No hay cliente registrado.")
                input("Presiona Enter para continuar...")
                continue

            ordenes = orden_service.obtener_ordenes_cliente(cliente_actual.id)
            if not ordenes:
                print("No hay órdenes registradas para este cliente.")
            else:
                print("--- ÓRDENES DEL CLIENTE ---")
                for orden in ordenes:
                    print(f"Orden #{orden.numero_orden} | {orden.plato} x{orden.cantidad} | ${orden.precio_total} | Pago: {orden.forma_pago} | Fecha: {orden.fecha}")

                num_imp = input("\n¿Desea imprimir alguna orden? Ingrese el número o 'n' para no: ").strip().lower()
                if num_imp.isdigit():
                    num_imp = int(num_imp)
                    orden_a_imprimir = next((o for o in ordenes if o.numero_orden == num_imp), None)
                    if orden_a_imprimir:
                        imprimir_orden(orden_a_imprimir)
            input("Presiona Enter para continuar...")

        elif opcion == "6":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")
            input("Presiona Enter para continuar...")
