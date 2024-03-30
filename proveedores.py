import random
import phonenumbers
import json
import os
from colorama import Fore
from email_validator import validate_email, EmailNotValidError


class Proveedores:

    def __init__(self, idProv, nom, ciu, dir, tel, email, anot):
        self.__idProveedor = idProv
        self.__nombre = nom
        self.__ciudad = ciu
        self.__direccion = dir
        self.__telefono = tel
        self.__email = email
        self.__anotacion = anot

    # <<COMANDOS>>
    def establecerIdProveedor(self):
        self.__idProveedor = 'F00' + str(random.randint(10, 90))
        return self.__idProveedor

    def establecerNombreProveedor(self, nom):
        self.__nombre = nom

    def establecerCiudadProveedor(self, ciu):
        self.__ciudad = ciu

    def establecerDireccionProveedor(self, dir):
        self.__direccion = dir

    def establecerTelefonoProveedor(self, tel):
        while True:
            try:
                numero = phonenumbers.parse(tel, None)
                if phonenumbers.is_valid_number(numero):
                    self.__telefono = tel
                    return True
            except phonenumbers.phonenumberutil.NumberParseException:
                return False

    def establecerEmailProveedor(self, email):
        while True:
            try:
                # Validar el correo electrónico
                validate_email(email)
                # El correo electrónico es válido, almacenarlo en el atributo __email
                self.__email = email
                return True
            except EmailNotValidError:
                return False

    def establecerAnotacionProveedor(self, anot):
        self.__anotacion = anot

    def agregarProveedorCompleto(self, idProv, nom, ciu, dir, tel, email, anot):
        dataProveedores = {'proveedores': []}
        if os.path.exists('proveedores.json') and os.path.getsize('proveedores.json') > 0:
            dataProveedores = Proveedores.cargarJson()

        if not nom or not ciu or not dir or not tel or not email or not anot:
            print('Todos los campos son obligatorios')
            return

        proveedorExiste = any(u["nombre"] == nom.lower() and
                              u["ciudad"] == ciu.lower() and
                              u["direccion"] == dir.lower()
                              for u in dataProveedores["proveedores"])
        if proveedorExiste:
            # REVISAR MOVER A MenuProveedores
            print(f'{Fore.RED}Este usuario ya se encuentra registrado{Fore.RESET}')

        dataProveedores['proveedores'].append({'id_proveedor': self.__idProveedor,
                                               'nombre': self.__nombre,
                                               'ciudad': self.__ciudad,
                                               'direccion': self.__direccion,
                                               'telefono': self.__telefono,
                                               'email': self.__email,
                                               'anotacion': self.__anotacion})

        Proveedores.guardarJson(dataProveedores)
        # REVISAR MOVER A MenuProveedores
        print(f'{Fore.GREEN}Proveedor agregado correctamente!{Fore.RESET}')

    def buscarProveedor():
        dataProveedores = Proveedores.cargarJson()
        # pide al usuario ingresar el apellido
        buscarProveedor = input(
            f'Ingrese apellido del cliente, "0" para regresar: ')
        if buscarProveedor == "0":
            return

        # almacena el apellido ingresado en la variable buscar
        buscar = buscarProveedor.lower()

        proveedoresEncontrados = []

        # recorre la palabra ingresada para verificar que coincida con alguno de los nombres de los proveedores
        for proveedor in dataProveedores['proveedores']:
            buscarNombreProveedor = proveedor['nombre'].lower()
            if all(palabra in buscarNombreProveedor for palabra in buscar):
                proveedoresEncontrados.append(proveedor)

        # si no se encontro el cliente
        if not proveedoresEncontrados:
            print(f'No se encontraron resultados')
            return

        # si se encontre el cliente, imprime los clientes con similitudes
        # y permite seleccionarlos segun el indice
        print(f'Proveedores encontrados:')
        for idx, proveedor in enumerate(proveedoresEncontrados, start=1):
            print(
                f'{idx}: {proveedor["nombre"].title()} - {proveedor["ciudad"].title()}')

        elegirIdx = int(input(f'Seleccione el proveedor: ')) - 1

        # si el indice seleccionado es menor a 0 o mayor al indice disponible retorna error, sino retorna el cliente seleccionado
        if elegirIdx < 0 or elegirIdx >= len(proveedoresEncontrados):
            print(f'Opcion invalida')
            return
        else:
            proveedorSeleccionado = proveedoresEncontrados[elegirIdx]
            proveedor = Proveedores(proveedorSeleccionado['id_proveedor'],
                                    proveedorSeleccionado['nombre'],
                                    proveedorSeleccionado['ciudad'],
                                    proveedorSeleccionado['direccion'],
                                    proveedorSeleccionado['telefono'],
                                    proveedorSeleccionado['email'],
                                    proveedorSeleccionado['anotacion'])

            return proveedor

    def editarProveedor(self):
        dataProveedor = Proveedores.cargarJson()

        # Usa enumerate para obtener el índice y el cliente
        for i, proveedor in enumerate(dataProveedor['proveedores']):
            # Compara el id_cliente del cliente con el self
            if proveedor['id_proveedor'] == self.obtenerIdProveedor():
                # Convierte el objeto Cliente a diccionario y actualiza el cliente en la lista
                dataProveedor['proveedores'][i] = self.toDict()
                break

        Proveedores.guardarJson(dataProveedor)

    def eliminarProveedor(self):
        dataProveedor = Proveedores.cargarJson()

        # Encuentra el cliente en la lista que tiene el mismo id_cliente que self
        proveedorAEliminar = None
        for proveedor in dataProveedor['proveedores']:
            if proveedor['id_proveedor'] == self.obtenerIdCliente():
                proveedorAEliminar = proveedor
                break

        # Si encontramos un cliente para eliminar, lo eliminamos de la lista
        if proveedorAEliminar is not None:
            dataProveedor['proveedores'].remove(proveedorAEliminar)

        Proveedores.guardarJson(dataProveedor)

    # <<CONSULTAS>>
    def obtenerIdProveedor(self):
        return self.__idProveedor

    def obtenerNombreProveedor(self):
        return self.__nombre

    def obtenerCiudadProveedor(self):
        return self.__ciudad

    def obtenerDireccionProveedor(self):
        return self.__direccion

    def obtenerTelefonoProveedor(self):
        return self.__telefono

    def obtenerEmailProveedor(self):
        return self.__email

    def obtenerAnotacionProveedor(self):
        return self.__anotacion

    def verProveedores():
        with open('proveedores.json', 'r') as archivoProveedores:
            dataProveedores = json.load(archivoProveedores)

        proveedoresLista = []

        for proveedor in dataProveedores['proveedores']:
            proveedor = Proveedores(proveedor['id_proveedor'],
                                    proveedor['nombre'],
                                    proveedor['ciudad'],
                                    proveedor['direccion'],
                                    proveedor['telefono'],
                                    proveedor['anotacion'])
            proveedoresLista.append(proveedor)
        return proveedoresLista

    # MANEJO ARCHIVO JSON
    def cargarJson():
        with open('proveedores.json', 'r') as archivoProveedores:
            dataProveedores = json.load(archivoProveedores)
            return dataProveedores

    def guardarJson(dataProveedores):
        with open('proveedores.json', 'w') as archivoProveedores:
            json.dump(dataProveedores, archivoProveedores, indent=4)

    def toDict(self):
        return {
            'id_proveedor': self.obtenerIdProveedor(),
            'nombre': self.obtenerNombreProveedor(),
            'ciudad': self.obtenerCiudadProveedor(),
            'direccion': self.obtenerDireccionProveedor(),
            'telefono': self.obtenerTelefonoProveedor(),
            'email': self.obtenerEmailProveedor(),
            'anotacion': self.obtenerAnotacionProveedor()
        }

    def __str__(self):
        return f'''Proveedor:
            ID: {self.obtenerIdProveedor()}
            Nombre: {self.obtenerNombreProveedor()}
            Ciudad: {self.obtenerCiudadProveedor()}
            Direccion: {self.obtenerDireccionProveedor()}
            Telefono: {self.obtenerTelefonoProveedor()}
            Email: {self.obtenerEmailProveedor()}
            Anotacion Importante: {self.obtenerAnotacionProveedor()}'''


'''proveedor = Proveedores(0, "", "", "", "", "")
proveedor.establecerIdProveedor()
proveedor.establecerNombreProveedor()
proveedor.establecerCiudadProveedor()
proveedor.establecerDireccionProveedor()
proveedor.establecerTelefonoProveedor()
proveedor.establecerAnotacionProveedor()

opcion = input(f'Confirmar proveedor S/N').lower()

if opcion == 's':
    proveedor.agregarProveedorCompleto(proveedor.obtenerIdProveedor(),
                               proveedor.obtenerNombreProveedor(),
                               proveedor.obtenerCiudadProveedor(),
                               proveedor.obtenerDireccionProveedor(),
                               proveedor.obtenerTelefonoProveedor(),
                               proveedor.obtenerAnotacionProveedor())'''


'''p = Proveedores("F0010", "Vida sana", "Buenos Aires", "Capital", "+5401115457895", "Buena calidad de productos")

print(p.__str__())

p.establecerNombreProveedor()
print(p.obtenerNombreProveedor())
p.establecerTelefonoProveedor()
print(p.obtenerTelefonoProveedor())

print(p.__str__())'''
