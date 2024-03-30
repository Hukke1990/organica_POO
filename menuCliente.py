import clientes
import tester
from colorama import Fore


class MenuCliente:

    def verClientes():
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}VER CLIENTES{Fore.RESET}')
        clientesLista = clientes.Cliente.verClientes()
        for i, c in enumerate(clientesLista, start=1):
            print(f'{i}: {Fore.GREEN}ID:{Fore.RESET} {c.obtenerIdCliente()}, {Fore.GREEN}Nombre y Apellido:{Fore.RESET} {c.obtenerNombreCliente().title()} {c.obtenerApellidoCliente().title()}, {Fore.GREEN}Ciudad:{Fore.RESET} {c.obtenerCiudadCliene().title()}')
        return input(f'\nPrecione una tecla para continuar')

    def agregarClientes(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}AGREGAR NUEVO CLIENTE{Fore.RESET}')
        cliente = clientes.Cliente(0, "", "", "", "", "", "")
        cliente.establecerIdCliente()
        nom = input(f'{Fore.GREEN}Nombre Cliente: {Fore.RESET}')
        cliente.establecerNombreCliente(nom)
        ape = input(f'{Fore.GREEN}Apellido Cliente: {Fore.RESET}')
        cliente.establecerApellidoCliente(ape)
        ciu = input(f'{Fore.GREEN}Ciudad Cliente: {Fore.RESET}')
        cliente.establecerCiudadCliente(ciu)
        dir = input(f'{Fore.GREEN}Direccion Cliente: {Fore.RESET}')
        cliente.establecerDireccionCliente(dir)
        while True:
            tel = input(f'{Fore.GREEN}Telefono Cliente: {Fore.RESET}')
            if cliente.establecerTelefonoCliente(tel):
                while True:
                    email = input(f'{Fore.GREEN}Email Cliente: {Fore.RESET}')
                    if cliente.establecerEmailCliente(email):
                        opcion = input(f'Confirmar cliente S/N: ').lower()
                        while True:
                            if opcion == 's':
                                cliente.agregarClienteCompleto(cliente.obtenerNombreCliente(),
                                                               cliente.obtenerApellidoCliente(),
                                                               cliente.obtenerCiudadCliene(),
                                                               cliente.obtenerDireccionCliente(),
                                                               cliente.obtenerTelefonoCliente(),
                                                               cliente.obtenerEmailCliente())
                                print(f'''Seleccione una opcion
                                                                    A: Agregar otro cliente
                                                                    F: Finalizar la carga''')
                                volverACargar = input(f'>> ').lower()
                                if volverACargar == 'a':
                                    MenuCliente.agregarClientes(self)
                                elif volverACargar == 'f':
                                    tester.MenuOrganica.menuClientes(self)

                            elif opcion == 'n':
                                print(f'Ha cancelado la carga del cliente.')
                                return tester.MenuOrganica.menuPrincial(self)
                    else:
                        print(f'El correo electronico no es valido')
            else:
                print(f'El numero de telefono no es valido. Intente de nuevo')
                continue

    def buscarClientes(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}BUSCAR CLIENTE{Fore.RESET}')
        clienteBuscar = []

        # verifica que el cliente excista, de ser asi lo agrega a la lista ClienteBuscar
        buscarCliente = clientes.Cliente.buscarCliente()
        if buscarCliente is not None:
            clienteBuscar.append(buscarCliente)

        tester.limpiarPantalla()
        print(f'{Fore.CYAN}CLIENTE ENCONTRADO{Fore.RESET}')
        for c in clienteBuscar:
            atributos = ["ID", "Nombre", "Apellido",
                         "Ciudad", "Direccion", "Telefono", "Email"]
        metodos = [c.obtenerIdCliente, c.obtenerNombreCliente, c.obtenerApellidoCliente,
                   c.obtenerCiudadCliene, c.obtenerDireccionCliente, c.obtenerTelefonoCliente, c.obtenerEmailCliente]
        for atributo, metodo in zip(atributos, metodos):
            try:
                print(f'{Fore.GREEN}{atributo}: {Fore.RESET}{metodo()}')
            except TypeError:
                print(f'Error: {metodo} no es un metodo valido')
        opcion = input(f'\nEditar cliente? S/N: ').lower()

        if opcion == 's':
            MenuCliente.editarCliente(self, clienteBuscar)
        elif opcion == 'n':
            return

        # este metodo es para imprimir los datos desde el .json
        '''for cliente in clienteBuscar:
                for key, value in cliente.items():                 
                        print(f'{key}: {value}')'''

    def editarCliente(self, clienteBuscar):
        camposModificados = []

        while True:
            tester.limpiarPantalla()
            print(f'{Fore.CYAN}EDICION DE CLIENTE{Fore.RESET}')
            print(f'Datos cliente')
            print('{:->35}'.format(''))  # agrega 35 lineas

            for c in clienteBuscar:
                atributos = ["ID", "Nombre", "Apellido",
                             "Ciudad", "Direccion", "Telefono", "Email"]
            metodos = [c.obtenerIdCliente, c.obtenerNombreCliente, c.obtenerApellidoCliente,
                       c.obtenerCiudadCliene, c.obtenerDireccionCliente, c.obtenerTelefonoCliente, c.obtenerEmailCliente]
            for atributo, metodo in zip(atributos, metodos):
                if atributo in camposModificados:
                    print(f'{Fore.CYAN}{atributo}: {Fore.RESET}{metodo()}')
                else:
                    print(f'{Fore.GREEN}{atributo}: {Fore.RESET}{metodo()}')
            print('\n')

            opcionEdicion = {
                1: "Editar Nombre",
                2: "Editar Apellido",
                3: "Editar Ciudad",
                4: "Editar Direccion",
                5: "Editar Telefono",
                6: "Editar Email",
                7: "Guardar Cambios",
                8: "Borrar",
                9: "Volver al menu anterior"
            }

            for opcion, mensaje in opcionEdicion.items():
                print(f'{opcion}: {mensaje}')

            try:
                opcion = int(input(f'Ingrese la opcion deseada: '))
            except ValueError:
                print(f'Opcion incorrecta')

            if opcion == 1:
                nuevoNombre = input(
                    f'Nuevo nombre, "c" para cancelar: ').lower()
                if nuevoNombre == "c":
                    continue
                else:
                    c.establecerNombreCliente(nuevoNombre)
                    camposModificados.append('Nombre')
            elif opcion == 2:
                nuevoApellido = input(
                    f'Nuevo apeliido, "c" para cancelar: ').lower()
                if nuevoApellido == "c":
                    continue
                else:
                    c.establecerApellidoCliente(nuevoApellido)
                    camposModificados.append('Apellido')
            elif opcion == 3:
                nuevaCiudad = input(
                    f'Nueva ciudad, "c" para cancelar: ').lower()
                if nuevaCiudad == "c":
                    continue
                else:
                    c.establecerCiudadCliente(nuevaCiudad)
                    camposModificados.append('Ciudad')
            elif opcion == 4:
                nuevaDireccion = input(
                    f'Nueva direccion, "c" para cancelar: ').lower()
                if nuevaCiudad == "c":
                    continue
                else:
                    c.establecerDireccionCliente(nuevaDireccion)
                    camposModificados.append('Direccion')
            elif opcion == 5:
                nuevoTelefono = input(
                    f'Nuevo telefono, "c" para cancelar: ').replace(" ", "")
                if nuevoTelefono == "c":
                    continue
                else:
                    if c.establecerTelefonoCliente(nuevoTelefono):
                        camposModificados.append('Telefono')
                    else:
                        print(f'{Fore.RED}Telefono invalido{Fore.RESET}')
                        input(f'precione ENTER para continuar')
            elif opcion == 6:
                nuevoEmail = input(
                    f'Nuevo email, "c" para cancelar: ').lower().replace(" ", "")
                if nuevoEmail == "c":
                    continue
                else:
                    if c.establecerEmailCliente(nuevoEmail):
                        camposModificados.append('Email')
                    else:
                        print(
                            f'{Fore.RED}El correo electronico no es valido{Fore.RESET}')
                        input(f'precione ENTER para continuar')
            elif opcion == 7:
                clientes.Cliente.editarCliente(c)
                print(f'\n{Fore.GREEN}Cliente modificado{Fore.RESET}')
                input(f'precione ENTER para continuar')

            elif opcion == 8:
                clientes.Cliente.eliminarCliente(c)
                print(f'\n{Fore.RED}Cliente eliminado{Fore.RESET}')
                input(f'precione ENTER para continuar')

            elif opcion == 9:
                tester.MenuOrganica.menuClientes(self)


# print(MenuCliente.verClientes())
