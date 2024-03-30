import random
import json
import os
from datetime import date, datetime
from colorama import Fore


class Productos:

    def __init__(self, idPro, nom, desc, pre, cat, pro, fec, cantDisp):
        self.__idProducto = idPro
        self.__nombre = nom
        self.__descripcion = desc
        self.__precio = pre
        self.__categoria = cat
        self.__proveedor = pro
        self.__fecha = fec
        self.__cantidadDisponible = cantDisp

    # <<COMANDOS>>
    def agregarProductoCompleto(self, nom, desc, pre, cat, pro, fec, cantDisp):
        dataProductos = {'productos': []}
        # verifica que exista el archivo json y que no este vacio:
        if os.path.exists('productos.json') and os.path.getsize('productos.json') > 0:
            dataProductos = Productos.cargarJson()

        # Verifica que todos los campos este completos
        if not nom or not desc or not pre or not cat or not pro or not fec or not cantDisp:
            print('Todos los campos son obligatorios!')
            return

        # recorrre el dic Productos para verificar si ya se encuentra cargado el producto
        productoExiste = any(p["nombre"] == nom.lower()
                             for p in dataProductos['productos'])

        if productoExiste:
            print(f'Este producto ya se encuentra en el stock')
            return

        dataProductos['productos'].append({'id_producto': self.__idProducto,
                                           'nombre': nom,
                                           'descripcion': desc,
                                           'precio': pre,
                                           'categoria': cat,
                                           'proveedor': pro,
                                           'fecha': fec,
                                           'cantidad_disponible': cantDisp})

        # Guardamos el diccionario en el archivo
        Productos.guardarJson(dataProductos)
        print(f'{Fore.GREEN}Producto agregado correctamente!{Fore.RESET}')

    def establecerIdProducto(self):
        self.__idProducto = 'P00' + str(random.randint(10, 90))
        return self.__idProducto

    def establecerNombreProducto(self, nom):
        self.__nombre = nom

    def establecerDescripcionProducto(self, desc):
        self.__descripcion = desc

    def establecerPrecioProducto(self, pre):
        try:
            if pre.isdigit():
                pre = float(pre)
                pre = round(pre, 2)
                self.__precio = float(pre)
                return True
        except ValueError:
            return False

    def establecerCategoriaProducto(self, cat):
        self.__categoria = cat

    def establecerProveedor(self, pro):
        self.__proveedor = pro

    def establecerFecha(self):
        self.__fecha = date.today()
        fecha = self.__fecha.strftime("%Y-%m-%d")
        return fecha

    def establecerFechaProducto(self, fec):
        try:
            datetime.strptime(fec, '%Y-%m-%d')
            self.__fecha = fec
            return True
        except ValueError:
            return False

    def establecerCantidadDisponible(self, cantDisp):
        try:
            if str(cantDisp).isdigit():
                self.__cantidadDisponible = int(cantDisp)
                return True
        except ValueError:
            return False

    def buscarProducto():
        dataProducto = Productos.cargarJson()
        # pide al usuario ingresar el apellido
        buscarProducto = input(
            f'Ingrese nombre del producto, "0" para regresar: ')
        if buscarProducto == "0":
            return

        buscar = buscarProducto.lower()

        productoEncontrados = []

        for producto in dataProducto['productos']:
            buscarProductoNombre = producto['nombre'].lower()
            # recorre la palabra ingresada para verificar que coincida con alguno de los nombres en el dicc Productos
            if all(palabra in buscarProductoNombre for palabra in buscar):
                productoEncontrados.append(producto)

        # si no se encontro el cliente
        if not productoEncontrados:
            return f'No se encontraron resultados'

        # si se encontre el cliente, imprime los clientes con similitudes
        # y permite seleccionarlos segun el indice
        print(f'Productos encontrados:')
        for idx, producto in enumerate(productoEncontrados, start=1):
            print(
                f'{idx}. {producto["nombre"].title()} - cantidad: {producto["cantidad_disponible"]}')

        elegirIdx = int(input(f'Seleccione el producto: ')) - 1

        # si el indice seleccionado es menor a 0 o mayor al indice disponible retorna error, sino retorna el cliente seleccionado
        if elegirIdx < 0 or elegirIdx >= len(productoEncontrados):
            print(f'Opcion invalida')
            return
        else:
            productoSeleccionado = productoEncontrados[elegirIdx]
            producto = Productos(productoSeleccionado['id_producto'],
                                 productoSeleccionado['nombre'],
                                 productoSeleccionado['descripcion'],
                                 productoSeleccionado['precio'],
                                 productoSeleccionado['categoria'],
                                 productoSeleccionado['proveedor'],
                                 productoSeleccionado['fecha'],
                                 productoSeleccionado['cantidad_disponible'])

            return producto

    def modificarPrecio():
        dataProductos = Productos.cargarJson()

        nuevoPrecio = float(input(f'Ingrese el % que desea aumentar: '))

        for i in dataProductos["productos"]:

            aumento = (i["precio"]) * (nuevoPrecio / 100)
            i["precio"] += aumento
            i["precio"] = round(i["precio"], 2)

        return dataProductos

    def editarProducto(self):
        dataProducto = Productos.cargarJson()

        for i, producto in enumerate(dataProducto['productos']):
            if producto['id_producto'] == self.obtenerIdProducto():
                dataProducto['productos'][i] = self.toDict()
                break

        Productos.guardarJson(dataProducto)

    def eliminiarProducto(self):
        dataProducto = Productos.cargarJson()

        productoAEliminar = None
        for producto in dataProducto['productos']:
            if producto['id_producto'] == self.obtenerIdProducto():
                productoAEliminar = producto
                break

        if productoAEliminar is not None:
            dataProducto['productos'].remove(productoAEliminar)

        Productos.guardarJson(dataProducto)

    # <<CONSULTAS>>
    def obtenerIdProducto(self):
        return self.__idProducto

    def obtenerNombreProducto(self):
        return self.__nombre

    def obtenerDescripcionProducto(self):
        return self.__descripcion

    def obtenerPrecioProducto(self):
        return self.__precio

    def obtenerCategoriaProducto(self):
        return self.__categoria

    def obtenerProveedor(self):
        return self.__proveedor

    def obtenerFechaJson(self):
        # Asumiendo que self.__fecha es una cadena en formato 'YYYY-MM-DD'
        fecha = datetime.strptime(self.__fecha, '%Y-%m-%d')

        # Ahora puedes usar strftime en fecha
        fecha_str = fecha.strftime("%Y-%m-%d")
        return fecha_str

    def obtenerFecha(self):
        return self.__fecha

    def obtenerCantidadDisponible(self):
        return self.__cantidadDisponible

    def verProductos():
        dataProducto = Productos.cargarJson()

        productoLista = []

        for producto in dataProducto['productos']:
            producto = Productos(producto['id_producto'],
                                 producto['nombre'],
                                 producto['descripcion'],
                                 producto['precio'],
                                 producto['categoria'],
                                 producto['proveedor'],
                                 producto['fecha'],
                                 producto['cantidad_disponible'])
            productoLista.append(producto)
        return productoLista

    # MANEJO ARCHIVO JSON

    def cargarJson():
        with open('productos.json', 'r') as archivoProductos:
            dataProductos = json.load(archivoProductos)
            return dataProductos

    def guardarJson(dataProductos):
        with open('productos.json', 'w') as archivoProductos:
            json.dump(dataProductos, archivoProductos, indent=4)

    def toDict(self):
        return {
            'id_producto': self.obtenerIdProducto(),
            'nombre': self.obtenerNombreProducto(),
            'descripcion': self.obtenerDescripcionProducto(),
            'precio': self.obtenerPrecioProducto(),
            'categoria': self.obtenerCategoriaProducto(),
            'proveedor': self.obtenerProveedor(),
            'fecha': self.obtenerFechaJson(),
            'cantidad_disponible': self.obtenerCantidadDisponible()
        }

    def __str__(self):
        return f'''Producto:
            ID: {self.obtenerIdProducto()}
            Nombre: {self.obtenerNombreProducto().capitalize()}
            Descripcion: {self.obtenerDescripcionProducto().capitalize()}
            Precio: {self.obtenerPrecioProducto()}
            Categoria: {self.obtenerCategoriaProducto().capitalize()}
            Proveedor: {self.obtenerProveedor().capitalize()}
            Fecha ingreso: {self.obtenerFecha()}
            Cantidad disponible: {self.obtenerCantidadDisponible()}'''


'''p = Productos.modificarPrecio()
print(p)'''
