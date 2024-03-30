import json
import random
import os
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from colorama import Fore
from difflib import get_close_matches


class Cliente:

    def __init__(self, idClie, nom, ape, ciu, dir, tel, email):
        self.__idCliente = idClie
        self.__nombre = nom
        self.__apellido = ape
        self.__ciudad = ciu
        self.__direccion = dir
        self.__telefono = tel
        self.__email = email

    # <<COMANDO>>
    def agregarClienteCompleto(self, nom, ape, ciu, dir, tel, email):
        dataCliente = {'clientes': []}
        # verifica que exista el archivo json y que no este vacio:
        if os.path.exists('clientes.json') and os.path.getsize('clientes.json') > 0:
            dataCliente = Cliente.cargarJson()

        # verifica que todos los campos esten completos
        if not nom or not ape or not dir or not tel or not email:
            print('Todos los campos son obligatorios!')
            return

        # recorre el dicc Clientes para verificar si ya se encuentra registrado el cliente
        clienteExiste = any(u["nombre"] == nom.lower() and
                            u["apellido"] == ape.lower() and
                            u["telefono"] == tel.replace(" ", "") and
                            u["email"] == email.replace(" ", "")
                            for u in dataCliente['clientes'])
        if clienteExiste:
            print(f'{Fore.RED}Este usuario ya se encuentra registrado{Fore.RESET}')
            return

        dataCliente['clientes'].append({'id_cliente': self.__idCliente,
                                        'nombre': nom,
                                        'apellido': ape,
                                        'ciudad': ciu,
                                        'direccion': dir,
                                        'telefono': tel,
                                        'email': email})

        # Guardamos el diccionario en el archivo
        Cliente.guardarJson(dataCliente)
        print(f'{Fore.GREEN}Cliente agregado correctamente!{Fore.RESET}')

    def establecerIdCliente(self):
        self.__idCliente = 'C00' + str(random.randint(10, 90))
        return self.__idCliente

    def establecerNombreCliente(self, nom):
        self.__nombre = nom

    def establecerApellidoCliente(self, ape):
        self.__apellido = ape

    def establecerCiudadCliente(self, ciu):
        self.__ciudad = ciu

    def establecerDireccionCliente(self, dir):
        self.__direccion = dir

    def establecerTelefonoCliente(self, tel):
        while True:
            try:
                numero = phonenumbers.parse(tel, None)
                if phonenumbers.is_valid_number(numero):
                    self.__telefono = tel
                    return True
            except phonenumbers.phonenumberutil.NumberParseException:
                return False

    def establecerEmailCliente(self, email):
        while True:
            try:
                # Validar el correo electrónico
                validate_email(email)
                # El correo electrónico es válido, almacenarlo en el atributo __email
                self.__email = email
                return True
            except EmailNotValidError:
                return False
                # El correo electrónico no es válido
                # print(f'Formato correo invalido, intente nuevamente!')
                # self.establecerEmailCliente()

    def buscarCliente():
        dataCliente = Cliente.cargarJson()

        buscarCliente = input(
            'Ingrese apellido del cliente, "0" para regresar: ')
        if buscarCliente == '0':
            return

        # almacena el apellido ingresado en la variable buscar
        buscar = buscarCliente.lower()

        clientesEncontrados = []

        # buscar el cliente utilizando la funcion get_close_matches para despues almacenarlos en la lista clientesEncontrados
        for cliente in dataCliente['clientes']:
            buscarApellidoCliente = cliente['apellido'].lower()
            similitud = get_close_matches(
                buscar, [buscarApellidoCliente], n=1, cutoff=0.6)

            if similitud:
                clientesEncontrados.append(cliente)

        if not clientesEncontrados:
            print('No se encontraron resultados')
            return

        print('Clientes encontrados:')
        for idx, cliente in enumerate(clientesEncontrados, start=1):
            print(
                f'{idx}. {cliente["apellido"].title()} {cliente["nombre"].title()}')

        while True:
            try:
                elegirIdx = int(input('Seleccione el cliente: ')) - 1
                if 0 <= elegirIdx < len(clientesEncontrados):
                    clienteSeleccionado = clientesEncontrados[elegirIdx]
                    cliente = Cliente(clienteSeleccionado['id_cliente'],
                                      clienteSeleccionado['nombre'],
                                      clienteSeleccionado['apellido'],
                                      clienteSeleccionado['ciudad'],
                                      clienteSeleccionado['direccion'],
                                      clienteSeleccionado['telefono'],
                                      clienteSeleccionado['email'])
                    return cliente
                else:
                    print('Opción inválida. Intente de nuevo.')
            except ValueError:
                print('Entrada inválida. Por favor, ingrese un número.')

    def editarCliente(self):
        dataCliente = Cliente.cargarJson()

        # Usa enumerate para obtener el índice y el cliente
        for i, cliente in enumerate(dataCliente['clientes']):
            # Compara el id_cliente del cliente con el self
            if cliente['id_cliente'] == self.obtenerIdCliente():
                # Convierte el objeto Cliente a diccionario y actualiza el cliente en la lista
                dataCliente['clientes'][i] = self.toDict()
                break

        Cliente.guardarJson(dataCliente)

    def eliminarCliente(self):
        dataCliente = Cliente.cargarJson()

        # Encuentra el cliente en la lista que tiene el mismo id_cliente que self
        clienteAeliminar = None
        for cliente in dataCliente['clientes']:
            if cliente['id_cliente'] == self.obtenerIdCliente():
                clienteAeliminar = cliente
                break

        # Si encontramos un cliente para eliminar, lo eliminamos de la lista
        if clienteAeliminar is not None:
            dataCliente['clientes'].remove(clienteAeliminar)

        Cliente.guardarJson(dataCliente)

    # <<CONSULTAS>>

    def obtenerIdCliente(self):
        return self.__idCliente

    def obtenerNombreCliente(self):
        return self.__nombre

    def obtenerApellidoCliente(self):
        return self.__apellido

    def obtenerCiudadCliene(self):
        return self.__ciudad

    def obtenerDireccionCliente(self):
        return self.__direccion

    def obtenerTelefonoCliente(self):
        return self.__telefono

    def obtenerEmailCliente(self):
        return self.__email

    def verClientes():
        dataClientes = Cliente.cargarJson()

        clientesLista = []

        for cliente in dataClientes['clientes']:
            cliente = Cliente(cliente['id_cliente'],  # transforma el cliente en un objeto
                              cliente['nombre'],
                              cliente['apellido'],
                              cliente['ciudad'],
                              cliente['direccion'],
                              cliente['telefono'],
                              cliente['email'])
            clientesLista.append(cliente)
        return clientesLista

    # MANEJO ARCHIVO JSON
    def cargarJson():
        with open('clientes.json', 'r') as archivoClientes:
            dataClientes = json.load(archivoClientes)
            return dataClientes

    def guardarJson(dataClientes):
        with open('clientes.json', 'w') as archivoClientes:
            json.dump(dataClientes, archivoClientes, indent=4)

    def toDict(self):
        return {
            'id_cliente': self.obtenerIdCliente(),
            'nombre': self.obtenerNombreCliente(),
            'apellido': self.obtenerApellidoCliente(),
            'ciudad': self.obtenerCiudadCliene(),
            'direccion': self.obtenerDireccionCliente(),
            'telefono': self.obtenerTelefonoCliente(),
            'email': self.obtenerEmailCliente()
        }

    def __str__(self):
        return f'''Cliente:
            ID: {self.obtenerIdCliente()}
            Nombre: {self.obtenerNombreCliente().title()}
            Apellido: {self.obtenerApellidoCliente().title()}
            Ciudad: {self.obtenerCiudadCliene().title()}
            Direccion: {self.obtenerDireccionCliente().title()}
            Telefono: {self.obtenerTelefonoCliente()}
            Email: {self.obtenerEmailCliente()}'''


c = Cliente.verClientes()
print(c)
