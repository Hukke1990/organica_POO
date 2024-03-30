import proveedores
import tester
from colorama import Fore


class MenuProveedor:

    def verProveedores():
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}VER PROVEEDORES{Fore.RESET}')
        proveedoresLista = proveedores.Proveedores.verProveedores()
        for i, p in enumerate(proveedoresLista, start=1):
            print(f'{i}: {Fore.GREEN}ID:{Fore.RESET} {p.obtenerIdProveedor()}, {Fore.GREEN}Nombre:{Fore.RESET} {p.obtenerNombreProveedor().title()}, {Fore.GREEN}Ciudad:{Fore.RESET} {p.obtenerCiudadProveedor().title()}')
        return input(f'\nPrecione una tecla para continuar')

    def agregarProvedores(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}AGREGAR NUEVO PROVEEDOR{Fore.RESET}')
        proveedor = proveedores.Proveedores(0, "", "", "", "", "", "")
        proveedor.establecerIdProveedor()
        nom = input(f'{Fore.GREEN}Nombre proveedor: {Fore.RESET}').lower()
        proveedor.establecerNombreProveedor(nom)
        ciu = input(f'{Fore.GREEN}Ciudad proveedor: {Fore.RESET}').lower()
        proveedor.establecerCiudadProveedor(ciu)
        dir = input(f'{Fore.GREEN}Direccion proveedor: {Fore.RESET}').lower()
        proveedor.establecerDireccionProveedor(dir)
        while True:
            tel = input(f'{Fore.GREEN}Telefono proveedor: {Fore.RESET}')
            if proveedor.establecerTelefonoProveedor(tel):
                while True:
                    email = input(f'{Fore.GREEN}Email proveedor: {Fore.RESET}')
                    if proveedor.establecerEmailProveedor(email):
                        anot = input(
                            f'{Fore.GREEN}Anotacion importante: {Fore.RESET}').lower()
                        proveedor.establecerAnotacionProveedor(anot)

                        opcion = input(f'Confirmar proveedor S/N').lower()

                        if opcion == 's':
                            proveedor.agregarProveedorCompleto(proveedor.obtenerIdProveedor(),
                                                               proveedor.obtenerNombreProveedor(),
                                                               proveedor.obtenerCiudadProveedor(),
                                                               proveedor.obtenerDireccionProveedor(),
                                                               proveedor.obtenerTelefonoProveedor(),
                                                               proveedor.obtenerEmailProveedor(),
                                                               proveedor.obtenerAnotacionProveedor())
                            print(f'''Seleccione una opcion
                                    A: Agregar otro proveedor
                                    F: Finalizar la carga''')
                            volverACargar = input(f'>> ').lower()
                            if volverACargar == 'a':
                                MenuProveedor.agregarProvedores(self)
                            elif volverACargar == 'f':
                                tester.MenuOrganica.menuProveedores(self)
                            else:
                                print(
                                    f'{Fore.RED}Opcion incorrecta{Fore.RESET}')
                                return

                        elif opcion == 'n':
                            print(
                                f'{Fore.RED}Ha cancelado la carga del proveedor{Fore.RESET}')
                            return tester.MenuOrganica.menuPrincipal()
                    else:
                        print(f'El correo electronico no es valido')
            else:
                print(f'El numero de telefono no es valido. Intente de nuevo')

    def buscarProveedores(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}BUSCAR PROVEEDOR{Fore.RESET}')
        proveedorBuscar = []

        buscarProveedor = proveedores.Proveedores.buscarProveedor()
        if buscarProveedor is not None:
            proveedorBuscar.append(buscarProveedor)

        tester.limpiarPantalla()
        print(f'{Fore.CYAN}PROVEEDOR ENCONTRADO{Fore.RESET}')
        for p in proveedorBuscar:
            atributos = ['ID', 'Nombre', 'Ciudad', 'Direccion',
                         'Telefono', 'Email', 'Anotacion Importante']
            metodos = [p.obtenerIdProveedor, p.obtenerNombreProveedor, p.obtenerCiudadProveedor,
                       p.obtenerDireccionProveedor, p.obtenerTelefonoProveedor, p.obtenerEmailProveedor, p.obtenerAnotacionProveedor]
            for atributo, metodo in zip(atributos, metodos):
                try:
                    print(f'{Fore.GREEN}{atributo}:{Fore.RESET} {metodo()}')
                except TypeError:
                    print(f'Error: {metodos} no es un metodo valido')

        opcion = input(f'\nEditar proveedor? S/N').lower()

        if opcion == 's':
            MenuProveedor.editarProveedor(self, proveedorBuscar)
        elif opcion == 'n':
            return

    def editarProveedor(self, proveedorBuscar):
        camposModificados = []

        while True:
            tester.limpiarPantalla()
            print(f'{Fore.CYAN}EDICION DE PROVEEDORES{Fore.RESET}')
            print(f'Datos proveedor')
            print('{:->35}'.format(''))  # agrega 35 lineas

            for p in proveedorBuscar:
                atributos = ['ID', 'Nombre', 'Ciudad', 'Direccion',
                             'Telefono', 'Email', 'Anotacion Importante']
                metodos = [p.obtenerIdProveedor, p.obtenerNombreProveedor, p.obtenerCiudadProveedor,
                           p.obtenerDireccionProveedor, p.obtenerTelefonoProveedor, p.obtenerEmailProveedor, p.obtenerAnotacionProveedor]
                for atributo, metodo in zip(atributos, metodos):
                    if atributo in camposModificados:
                        print(f'{Fore.CYAN}{atributo}:{Fore.RESET} {metodo()}')
                    else:
                        print(f'{Fore.GREEN}{atributo}:{Fore.RESET} {metodo()}')
                print(f'\n')

                opcionEdicion = {
                    1: 'Editar nombre',
                    2: 'Editar ciudad',
                    3: 'Editar direccion',
                    4: 'Editar telefono',
                    5: 'Editar email',
                    6: 'Editar anotacion',
                    7: 'Guardar cambios',
                    8: 'Eliminar proveedor',
                    9: 'Volver al manu anterior'
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
                    if nuevoNombre == 'c':
                        continue
                    else:
                        p.establecerNombreProveedor(nuevoNombre)
                        camposModificados.append('Nombre')
                elif opcion == 2:
                    nuevaCiudad = input(
                        f'Nueva ciudad, "c" para cancelar: ').lower()
                    if nuevaCiudad == 'c':
                        continue
                    else:
                        p.establecerCiudadProveedor(nuevaCiudad)
                        camposModificados.append('Ciudad')
                elif opcion == 3:
                    nuevaDireccion = input(
                        f'Nueva direccion, "c" para cancelar: ').lower()
                    if nuevaDireccion == 'c':
                        continue
                    else:
                        p.establecerDireccionProveedor(nuevaDireccion)
                        camposModificados.append('Direccion')
                elif opcion == 4:
                    nuevoTelefono = input(
                        f'Nuevo telefono, "c" para cancelar: ').replace(" ", "")
                    if nuevoTelefono == 'c':
                        continue
                    else:
                        if p.establecerTelefonoProveedor(nuevoTelefono):
                            camposModificados.append('Telefono')
                        else:
                            print(f'{Fore.RED}Telefono invalido{Fore.RESET}')
                            input(f'precione ENTER para continuar: ')
                elif opcion == 5:
                    nuevoEmail = input(
                        f'Nuevo email, "c" para cancelar').replace(" ", "")
                    if nuevoEmail == 'c':
                        continue
                    else:
                        if p.establecerEmailProveedor(nuevoEmail):
                            camposModificados.append(nuevoEmail)
                        else:
                            print(
                                f'{Fore.RED}El correo electronico no es valido{Fore.RESET}')
                            input(f'precione ENTER para continuar')
                elif opcion == 6:
                    nuevaAnotacion = input(
                        f'Nueva anotacion, "c" para cancelar').lower()
                    if nuevaAnotacion == 'c':
                        continue
                    else:
                        p.establecerAnotacionProveedor(nuevaAnotacion)
                        camposModificados.append('Anotacion Importante')
                elif opcion == 7:
                    proveedores.Proveedores.editarProveedor(p)
                    print(f'\n{Fore.GREEN}Proveedor modificado{Fore.RESET}')
                    input(f'precione ENTER para continuar')
                elif opcion == 8:
                    proveedores.Proveedores.eliminarProveedor(p)
                    print(f'\n{Fore.RED}Proveedor eliminado{Fore.RESET}')
                    input(f'precione ENTER para continuar')

                elif opcion == 9:
                    tester.MenuOrganica.menuProveedores(self)


# print(MenuProveedor.editarProveedor())
