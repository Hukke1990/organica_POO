import menuProductos
import menuCliente
import menuProveedores
import menuUsuario
from menuUsuario import usuarios
import ventas
from colorama import Fore, Back, Style
from datetime import datetime
import platform
import os


def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
              "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)

    return messsage


now = datetime.now()


def limpiarPantalla():  # limpiar la consola completa
    sistema_operativo = platform.system()
    if sistema_operativo == "Windows":
        os.system("cls")
    else:
        os.system("clear")


class MenuOrganica:
    # LOG IN
    def main(self):
        limpiarPantalla()
        print(f'{Fore.CYAN}BIENVENIDOS A ORGANICA{Fore.RESET}')
        print(f'Para poder utilizar esta aplicacion debe conectarse con su cuenta\n')
        print(f'1: Conectarse')
        print(f'2: Registrarse')

        while True:
            opcion = input(f'>> ')

            if opcion == '1':
                menuUsuario.MenuUsuario.conectarse(self)
            elif opcion == '2':
                menuUsuario.MenuUsuario.registrarse(self)
            else:
                print(f'Opcion invalida!')

    # VALIDACION ROL USUARIO

    def menuPrincial(self, usuarioActual):
        while True:
            limpiarPantalla()
            print(current_date_format(now))
            print(f'{Fore.CYAN}NOTICIAS DEL DIA{Fore.RESET}')
            print(menuProductos.MenuProductos.obtenerControlStock(self))
            print(f'{Fore.CYAN}MENU PRINCIPAL{Fore.RESET}')
            print(f'1. Menu Clientes')
            print(f'2. Menu Productos')
            print(f'3. Menu Proveedores')
            print(f'4. Menu Ventas')
            print(f'5. Menu Administrador')
            print(f'6. Salir de la cuenta')

            opcion = input(f'\nIngrese una opcion: ')

            if opcion.isdigit():
                if opcion == '1':
                    self.menuClientes(usuarioActual)
                elif opcion == '2':
                    self.menuProductos(usuarioActual)
                elif opcion == '3':
                    self.menuProveedores(usuarioActual)
                elif opcion == '4':
                    self.menuVentas(usuarioActual)
                elif opcion == '5':
                    self.menuAdministrador(usuarioActual)
                elif opcion == '6':
                    self.main()

    def menuClientes(self, usuarioActual):
        while True:
            limpiarPantalla()
            print(f'{Fore.CYAN}MENU CLIENTES{Fore.RESET}')
            print(f'1: Ver Clientes')
            print(f'2: Buscar Cliente')
            print(f'3: Agrega Cliente')
            print(f'4: Menu Principal')
            opcion = input(f'Ingrese una opcion: ')

            if opcion == '1':
                menuCliente.MenuCliente.verClientes()
            elif opcion == '2':
                menuCliente.MenuCliente.buscarClientes(self, usuarioActual)
            elif opcion == '3':
                menuCliente.MenuCliente.agregarClientes(self, usuarioActual)
            elif opcion == '4':
                self.menuPrincial(usuarioActual)

    def menuProductos(self, usuarioActual):
        while True:
            limpiarPantalla()
            print(f'{Fore.CYAN}MENU PRODUCTOS{Fore.RESET}')
            print(f'1: Ver Productos')
            print(f'2: Buscar Producto')
            print(f'3: Agrega Producto')
            print(f'4: Modificar precios generales')
            print(f'5: Menu Principal')
            opcion = input(f'Ingrese una opcion: ')

            if opcion == '1':
                menuProductos.MenuProductos.verProductos()
            elif opcion == '2':
                menuProductos.MenuProductos.buscarProducto(self, usuarioActual)
            elif opcion == '3':
                menuProductos.MenuProductos.agregarProductos(self)
            elif opcion == '4':
                menuProductos.MenuProductos.modificarPrecio()
            elif opcion == '5':
                self.menuPrincial(usuarioActual)

    def menuProveedores(self, usuarioActual):
        while True:
            limpiarPantalla()
            print(f'{Fore.CYAN}MENU PROVEEDORES{Fore.RESET}')
            print(f'1: Ver Proveedores')
            print(f'2: Buscar Proveedor')
            print(f'3: Agrega Proveedor')
            print(f'4: Menu Principal')
            opcion = input(f'Ingrese una opcion: ')

            if opcion == '1':
                menuProveedores.MenuProveedor.verProveedores()
            elif opcion == '2':
                menuProveedores.MenuProveedor.buscarProveedores(self, usuarioActual)
            elif opcion == '3':
                menuProveedores.MenuProveedor.agregarProvedores(self)
            elif opcion == '4':
                self.menuPrincial(usuarioActual)

    def menuVentas(self, usuarioActual):
        limpiarPantalla()
        print(f'{Fore.CYAN}MENU VENTAS{Fore.RESET}')
        print(f'1. Realizar Venta')
        print(f'2. Ver historial de ventas')
        print(f'3. Ver mejores clientes')
        print(f'4. Ver hisotiral de compras del cliente')
        print(f'5. Generar informa productos mas vendidos')
        print(f'6. Volver al menu principal')

        opcion = input(
            f'\n{Fore.GREEN}Ingrese una opcion: {Fore.RESET}')

        if opcion == '1':
            ventas.Ventas.realizarVentas(self)
        elif opcion == '2':
            ventas.Ventas.verHistorialVentas(self)
        elif opcion == '3':
            ventas.Ventas.verMejoresClientes(self)
        elif opcion == '4':
            ventas.Ventas.verHistorialComprasCliente(self)
        elif opcion == '5':
            ventas.Ventas.verProductosMasVendidos(self)
        elif opcion == '6':
            self.menuPrincial(usuarioActual)

    def menuAdministrador(self, usuarioActual):
        if usuarioActual['id_rol'] == "usuario":
            limpiarPantalla()
            print(f'{Fore.RED}No tiene acceso al menu administrador{Fore.RESET}')
            input(f'\nPrecione una tecla para continuar')
            self.menuPrincial(usuarioActual)

        elif usuarioActual['id_rol'] == "administrador":
            while True:
                limpiarPantalla()
                print(f'{Fore.CYAN}MENU ADMINISTRADOR{Fore.RESET}')
                print(f'1. Ver usuarios')
                print(f'2. Modificar usuarios')
                print(f'3. Salir del menu')

                opcion = input(
                    f'\n{Fore.GREEN}Ingrese una opcion: {Fore.RESET}')

                if opcion == '1':
                    menuUsuario.MenuUsuario.verUsuarios()
                elif opcion == '2':
                    usuarios.Usuario.buscarUsuario(self)
                elif opcion == '3':
                    self.menuPrincial(usuarioActual)
                    break


if __name__ == '__main__':
    test = MenuOrganica()
    test.main()
