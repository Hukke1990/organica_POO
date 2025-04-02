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

    def agregarClientes(self, usuarioActual):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}AGREGAR NUEVO CLIENTE{Fore.RESET}')
        cliente = clientes.Cliente(0, "", "", "", "", "", "")
        cliente.establecerIdCliente()

        # Función auxiliar para manejar la cancelación
        def cancelar_operacion():
            print(f'{Fore.RED}Operación cancelada por el usuario.{Fore.RESET}')
            return tester.MenuOrganica.menuPrincial(self, usuarioActual)

        # Solicitar datos con posibilidad de cancelar
        nom = input(f'{Fore.GREEN}Nombre Cliente (o "C" para cancelar): {Fore.RESET}')
        if nom.lower() == 'c':
            return cancelar_operacion()
        cliente.establecerNombreCliente(nom)

        ape = input(f'{Fore.GREEN}Apellido Cliente (o "C" para cancelar): {Fore.RESET}')
        if ape.lower() == 'c':
            return cancelar_operacion()
        cliente.establecerApellidoCliente(ape)

        ciu = input(f'{Fore.GREEN}Ciudad Cliente (o "C" para cancelar): {Fore.RESET}')
        if ciu.lower() == 'c':
            return cancelar_operacion()
        cliente.establecerCiudadCliente(ciu)

        dir = input(f'{Fore.GREEN}Direccion Cliente (o "C" para cancelar): {Fore.RESET}')
        if dir.lower() == 'c':
            return cancelar_operacion()
        cliente.establecerDireccionCliente(dir)

        while True:
            tel = input(f'{Fore.GREEN}Telefono Cliente (o "C" para cancelar): {Fore.RESET}')
            if tel.lower() == 'c':
                return cancelar_operacion()
            if cliente.establecerTelefonoCliente(tel):
                while True:
                    email = input(f'{Fore.GREEN}Email Cliente (o "C" para cancelar): {Fore.RESET}')
                    if email.lower() == 'c':
                        return cancelar_operacion()
                    if cliente.establecerEmailCliente(email):
                        opcion = input(f'Confirmar cliente S/N (o "C" para cancelar): ').lower()
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
                                    return tester.MenuOrganica.menuClientes(self)

                            elif opcion == 'n':
                                print(f'Ha cancelado la carga del cliente.')
                                return tester.MenuOrganica.menuPrincial(self)
                    else:
                        print(f'El correo electronico no es valido')
            else:
                print(f'El numero de telefono no es valido. Intente de nuevo')
                continue

    def buscarClientes(self, usuarioActual):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}BUSCAR CLIENTE{Fore.RESET}')
        clienteBuscar = []
    
        # Verifica que el cliente exista, de ser así lo agrega a la lista clienteBuscar
        buscarCliente = clientes.Cliente.buscarCliente()
        if buscarCliente is not None:
            clienteBuscar.append(buscarCliente)
    
        if not clienteBuscar:
            print(f'{Fore.RED}No se encontró ningún cliente.{Fore.RESET}')
            return
    
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
                    print(f'Error: {metodo} no es un método válido')
    
        opcion = input(f'\nEditar cliente? S/N: ').lower()
    
        if opcion == 's':
            MenuCliente.editarCliente(self, clienteBuscar, usuarioActual)
        elif opcion == 'n':
            return

    def editarCliente(self, clienteBuscar, usuarioActual):
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
                tester.MenuOrganica.menuClientes(self, usuarioActual)


# print(MenuCliente.verClientes())
