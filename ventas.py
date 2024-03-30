import json
import os
from datetime import *
from colorama import Fore
import tester
import productos
import clientes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Ventas(productos.Productos, clientes.Cliente):

    '''    
        def menuVentas():
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}MENU VENTAS{Fore.RESET}')
        print(f'1. Realizar Venta')
        print(f'2. Buscar Venta')
        print(f'3. Ver historial ventas')
        print(f'4. Ver historial cliente')
        print(f'5. Generar informa productos mas vendidos')
        print(f'6. Generar informa clientes compras')
        print(f'7. Volver al menu principal')

        option = input(f'{Fore.GREEN}Ingrese una opcion: {Fore.RESET}')

        if option == '1':
            Ventas.realizarVentas()
        elif option == '2':
            Ventas.buscarVentas()
        elif option == '3':
            pass
        elif option == '4':
            pass
        elif option == '5':
            pass
        elif option == '6':
            pass
        elif option == '7':
            tester.MenuOrganica.menuPrincial()
    '''

    def buscarVentas(self):
        pass

    def realizarVentas(self):
        tester.limpiarPantalla()
        dataVentas = {'ventas': []}
        # carga el JSON de ventas
        if os.path.exists('ventas.json') and os.path.getsize('ventas.json') > 0:
            dataVentas = Ventas.cargarJson()
        # carga el JSON de clientes
        dataClientes = clientes.Cliente.cargarJson()
        dataProducto = productos.Productos.cargarJson()

        try:
            apellido = input(
                f'{Fore.GREEN}Ingrese el apellido del cliente: {Fore.RESET}').lower()
            print()
            buscarApellido = apellido

            clientesSimilares = []

            for cliente in dataClientes['clientes']:
                encontrarApellido = cliente['apellido'].lower()
                if all(apellido in encontrarApellido for apellido in buscarApellido):
                    if cliente['apellido'].lower() == buscarApellido:
                        clientesSimilares.append(cliente)

            if not clientesSimilares:
                raise ValueError('No se encontraron resultados')

            for i, cliente in enumerate(clientesSimilares, start=1):
                print(
                    f'{i}. {Fore.GREEN}Nombre:{Fore.RESET} {cliente["nombre"]} - {Fore.GREEN}Apellido:{Fore.RESET}{cliente["apellido"]}')

            seleccionarCliente = int(input('\nSeleccione el cliente: ')) - 1

            if seleccionarCliente < 0 or seleccionarCliente >= len(clientesSimilares):
                print('Opcion invalida')
                return
        except ValueError as e:
            print(f'{Fore.RED}Error: {Fore.RESET}{str(e)}')
            return

        cliente = clientesSimilares[seleccionarCliente]

        # SELECCION DE PRODUCTO!
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}SELECCIONE PRODUCTO{Fore.RESET}')
        print(
            f'{Fore.GREEN}Cliente seleccionado:{Fore.RESET} {cliente["nombre"].title()} {cliente["apellido"].title()}\n')
        for producto in dataProducto['productos']:
            print(f'{producto["id_producto"]} - {producto["nombre"]}')
        productosVenta = []

        # productoActual = None  # Valor inicial
        continuar = True
        while continuar:
            seleccionarProducto = input(
                f'\n{Fore.GREEN}Seleccione el ID del producto a vender (0 para finalizar): {Fore.RESET}')

            if seleccionarProducto == '0':
                continuar = False
            else:
                producto = next(
                    (p for p in dataProducto['productos'] if p['id_producto'] == seleccionarProducto), None)
                if producto:
                    try:
                        cantidadVenta = int(
                            input(f'{Fore.GREEN}Ingrese la cantidad de "{Fore.RESET}{producto["nombre"]}{Fore.RESET}{Fore.GREEN}": {Fore.RESET}'))
                        if cantidadVenta <= producto["cantidad_disponible"]:
                            producto["cantidad_disponible"] -= cantidadVenta
                            producto["cantidad_venta"] = cantidadVenta
                            productosVenta.append(producto)
                            print(
                                f'{cantidadVenta} unidades de "{producto["nombre"]}" agregadas al carrito de compras.')
                        else:
                            print(
                                f'\n{Fore.RED}Error: {Fore.RESET}No hay suficientes productos disponibles.')
                    except ValueError:
                        print(
                            f'\n{Fore.RED}Error: {Fore.RESET}La cantidad ingresada no es válida.')
                else:
                    print(
                        f'\n{Fore.RED}Error: {Fore.RESET}El producto no existe.')

        # CALCULA EL TOTAL DE LA VENTA Y MUESTRA DETALLES
        totalVenta = 0.0

        for producto in productosVenta:
            nombreProducto = producto['nombre']
            precioProducto = producto['precio']
            subtotal = precioProducto * cantidadVenta
            print('\n{:->35}'.format(''))
            print(
                f'{Fore.GREEN}Producto:{Fore.RESET} {nombreProducto} - {Fore.GREEN}Precio: {Fore.RESET}${precioProducto} - {Fore.GREEN}Cantidad: {Fore.RESET}{cantidadVenta} - {Fore.GREEN}Subtotal: {Fore.RESET}${subtotal}')
            totalVenta += subtotal
            print(f'{Fore.GREEN}Total de la venta: {Fore.RESET}${totalVenta}')

        # AGREGAR DESCUENTO A LA VENTA
        try:
            descuento = int(
                input(f'{Fore.GREEN}Ingrese el porcentaje de descuento a aplicar: {Fore.RESET}'))
            CantidadDescuento = 0.0

            if descuento > 0.0:
                CantidadDescuento = totalVenta * (descuento / 100)
                totalVenta -= CantidadDescuento
                print(
                    f'{Fore.GREEN}Descuento aplicado: {Fore.RESET}{descuento}% - {Fore.GREEN}Cantidad:{Fore.RESET} ${CantidadDescuento}')
            else:
                print(f'{Fore.CYAN}Descuento aplicado:{Fore.CYAN} 0%')
        except ValueError:
            print(
                f'\n{Fore.RED}Error: {Fore.RESET}El descuento ingresado no es válido.')
            return

        # ACTUALIZAR LA CANTIDAD DISPONIBLE DE LOS PRODUCTOS
        '''for producto in productosVenta:
            cantidadVenta = producto.pop('cantidad_venta', None)'''
        productos.Productos.guardarJson(dataProducto)

        # GUARDA EL JSON DE VENTAS
        dataVentas['ventas'].append({
            'id_venta': int(len(dataVentas.get('ventas', []))) + 1,
            'id_cliente': cliente['id_cliente'],
            'nombre_cliente': cliente['nombre'] + ' ' + cliente['apellido'],
            'fecha': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'descuento_%': float(descuento),
            'descuento_aplicado': round(CantidadDescuento, 2),
            'total_venta': round(totalVenta, 2),
            'total_venta_descuento': round(CantidadDescuento, 2),
            'productos': productosVenta
        })

        Ventas.guardarJson(dataVentas)

        print('{:->35}'.format(''))
        print(f'{Fore.GREEN}Total de la venta: {Fore.RESET}${totalVenta}')
        print('{:->35}'.format(''))

        print('Gracias por su compra')

        input(f'\n{Fore.CYAN}Presione ENTER para continuar{Fore.RESET}')
        tester.MenuOrganica.menuVentas(self)

    def verHistorialVentas(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}HISTORIAL VENTAS{Fore.RESET}')
        dataVentas = Ventas.cargarJson()

        for venta in dataVentas['ventas']:
            print('{:->35}'.format(''))
            print(f'{Fore.GREEN}ID VENTA: {Fore.RESET}{venta["id_venta"]}')
            print(f'{Fore.GREEN}ID CLIENTE: {Fore.RESET}{venta["id_cliente"]}')
            print(
                f'{Fore.GREEN}NOMBRE CLIENTE: {Fore.RESET}{venta["nombre_cliente"]}')
            print(f'{Fore.GREEN}FECHA: {Fore.RESET}{venta["fecha"]}')
            print(
                f'{Fore.GREEN}DESCUENTO: {Fore.RESET}{venta["descuento_%"]} %')
            print(
                f'{Fore.GREEN}DESCUENTO APLICADO: {Fore.RESET}${venta["descuento_aplicado"]}')
            print(
                f'{Fore.GREEN}TOTAL VENTA: {Fore.RESET}${venta["total_venta"]}')
            print(
                f'{Fore.GREEN}TOTAL VENTA DESCUENTO: {Fore.RESET}${venta["total_venta_descuento"]}')
            print(f'{Fore.GREEN}PRODUCTOS: {Fore.RESET}')
            for producto in venta["productos"]:
                print(
                    f'{Fore.GREEN} - {Fore.RESET}{producto["nombre"]} {Fore.GREEN}cantidad: {Fore.RESET}{producto["cantidad_venta"]}pza')

        input(f'\n{Fore.CYAN}Presione ENTER para continuar{Fore.RESET}')

    def verHistorialClientes(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}HISTORIAL VENTAS{Fore.RESET}')
        dataVentas = Ventas.cargarJson()

        for venta in dataVentas['ventas']:
            print('{:->35}'.format(''))
            print(f'{Fore.GREEN}ID VENTA: {Fore.RESET}{venta["id_venta"]}')
            print(f'{Fore.GREEN}ID CLIENTE: {Fore.RESET}{venta["id_cliente"]}')
            print(
                f'{Fore.GREEN}NOMBRE CLIENTE: {Fore.RESET}{venta["nombre_cliente"]}')
            print(f'{Fore.GREEN}FECHA: {Fore.RESET}{venta["fecha"]}')
            print(
                f'{Fore.GREEN}DESCUENTO: {Fore.RESET}{venta["descuento_%"]} %')
            print(
                f'{Fore.GREEN}DESCUENTO APLICADO: {Fore.RESET}${venta["descuento_aplicado"]}')
            print(
                f'{Fore.GREEN}TOTAL VENTA: {Fore.RESET}${venta["total_venta"]}')
            print(
                f'{Fore.GREEN}TOTAL VENTA DESCUENTO: {Fore.RESET}${venta["total_venta_descuento"]}')
            print(f'{Fore.GREEN}PRODUCTOS: {Fore.RESET}')
            for producto in venta["productos"]:
                print(
                    f'{Fore.GREEN} - {Fore.RESET}{producto["nombre"]} {Fore.GREEN}cantidad: {Fore.RESET}{producto["cantidad_venta"]}pza')

        input(f'\n{Fore.CYAN}Presione ENTER para continuar{Fore.RESET}')

    def verMejoresClientes(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}INFORME CLIENTES MAS VENDIDOS{Fore.RESET}')
        dataVentas = Ventas.cargarJson()
        informeClientes = {}

        for venta in dataVentas['ventas']:
            clienteId = venta['id_cliente']
            if clienteId in informeClientes:
                informeClientes[clienteId] += 1
            else:
                informeClientes[clienteId] = 1

        clientesOrdenados = sorted(
            informeClientes, key=informeClientes.get, reverse=True)

        print('{:->35}'.format(''))
        for clienteId in clientesOrdenados:
            for venta in dataVentas['ventas']:
                if venta['id_cliente'] == clienteId:
                    nombreCliente = venta['nombre_cliente'].title()
                    print(f'{Fore.GREEN}ID CLIENTE: {Fore.RESET}{clienteId}')
                    print(
                        f'{Fore.GREEN}NOMBRE CLIENTE: {Fore.RESET}{nombreCliente}')
                    print(
                        f'{Fore.GREEN}COMPRAS: {Fore.RESET}{informeClientes[clienteId]}')
                    print('{:->35}'.format(''))
                    break

        input(f'\n{Fore.CYAN}Presione ENTER para continuar{Fore.RESET}')

    def verProductosMasVendidos(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}INFORME PRODUCTOS MAS VENDIDOS{Fore.RESET}')
        dataVentas = Ventas.cargarJson()
        informeProductos = {}

        for venta in dataVentas['ventas']:
            for producto in venta['productos']:
                nombreProducto = producto['nombre']
                if nombreProducto in informeProductos:
                    informeProductos[nombreProducto] += 1
                else:
                    informeProductos[nombreProducto] = 1

        productosOrdenados = sorted(
            informeProductos, key=informeProductos.get, reverse=True)

        print('{:->35}'.format(''))
        for producto in productosOrdenados:
            print(f'{Fore.GREEN}PRODUCTO: {Fore.RESET}{producto}')
            print(
                f'{Fore.GREEN}COMPRAS: {Fore.RESET}{informeProductos[producto]}')
            print('{:->35}'.format(''))

        input(f'\n{Fore.CYAN}Presione ENTER para continuar{Fore.RESET}')

    def verHistorialComprasCliente(self):
        try:
            tester.limpiarPantalla()
            print(f'{Fore.CYAN}HISTORIAL COMPRAS CLIENTE{Fore.RESET}')
            dataVentas = Ventas.cargarJson()

            buscarCliente = input(
                f'{Fore.GREEN}Apellido del ciente, "0" para volver al menu: {Fore.RESET}')

            palabrasBusqueda = buscarCliente.lower().split()

            if buscarCliente == "0":
                tester.MenuOrganica.menuVentas()

            clientesCoincidentes = {}

            for cliente in dataVentas['ventas']:
                nombreCliente = cliente['nombre_cliente'].lower()

                if all(palabra in nombreCliente for palabra in palabrasBusqueda):
                    if nombreCliente not in clientesCoincidentes:
                        clientesCoincidentes[nombreCliente] = [cliente]
                    else:
                        clientesCoincidentes[nombreCliente].append(cliente)

            print(f'{Fore.CYAN}CLIENTES COINCIDENTES: {Fore.RESET}')
            for i, cliente in enumerate(clientesCoincidentes.keys(), start=1):
                print(f'{Fore.GREEN}{i}. {Fore.RESET}{cliente.title()}')

            seleccionarCliente = int(
                input(f'\n{Fore.CYAN}Seleccione el cliente: {Fore.RESET}')) - 1

            clientesEncontrados = list(clientesCoincidentes.values())
            if seleccionarCliente < 0 or seleccionarCliente >= len(clientesEncontrados):
                print(f'{Fore.RED}Error: {Fore.RESET}Opcion invalida')

            clienteSeleccionado = clientesEncontrados[seleccionarCliente]

            tester.limpiarPantalla()
            print(
                f'{Fore.CYAN}HISTORIAL DE COMPRAS DEL CLIENTE: {Fore.RESET}{clienteSeleccionado[0]["nombre_cliente"].title()}')
            for venta in clienteSeleccionado:
                print('{:->35}'.format(''))
                print(f'{Fore.GREEN}FECHA: {Fore.RESET}{venta["fecha"]}')
                print(f'{Fore.GREEN}PRODUCTOS: {Fore.RESET}')
                for producto in venta['productos']:
                    print(
                        f' - {producto["nombre"]} - {Fore.GREEN}CANTIDAD: {Fore.RESET}{producto["cantidad_venta"]}')
                if venta['descuento_%'] == 0.0:
                    print(f'{Fore.GREEN}DESCUENTO: {Fore.RESET}No aplicado')
                else:
                    print(
                        f'{Fore.GREEN}DESCUENTO: {Fore.RESET}{venta["descuento_aplicado"]}')
                print(f'{Fore.GREEN}TOTAL: {Fore.RESET}{venta["total_venta"]}')

            input(f'\n{Fore.CYAN}Presione ENTER para continuar{Fore.RESET}')
        except Exception as e:
            print(f'Error: {str(e)}')

    # REVISAR!!!
    '''def enviar_email_compra(correo_comprador, datos_compra):
        # Configuración del correo
        mi_correo = 'tu_correo@gmail.com'
        mi_contraseña = 'tu_contraseña'

        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = mi_correo
        msg['To'] = correo_comprador
        msg['Subject'] = 'Detalles de tu compra'

        # Agregar los datos de la compra al mensaje
        cuerpo_mensaje = 'Hola,\n\nAquí están los detalles de tu compra:\n' + datos_compra
        msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

        # Iniciar servidor y enviar correo
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(mi_correo, mi_contraseña)
        text = msg.as_string()
        server.sendmail(mi_correo, correo_comprador, text)
        server.quit()'''

# Ejemplo de uso
# enviar_email_compra('correo_del_comprador@ejemplo.com', 'datos_de_compra')


# MANEJO ARCHIVO JSON

    def cargarJson():
        with open('ventas.json', 'r') as archivoVentas:
            dataVentas = json.load(archivoVentas)
            return dataVentas

    def guardarJson(dataVentas):
        with open('ventas.json', 'w') as archivoVentas:
            json.dump(dataVentas, archivoVentas, indent=4)
