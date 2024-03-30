from colorama import Fore
import usuarios
import tester


class MenuUsuario:

    def registrarse(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}REGISTRO{Fore.RESET}')
        usuario = usuarios.Usuario(0, "", "", "", "")
        usuario.establecerIdUsuario()
        usu = input(f'{Fore.GREEN}Nombre Usuario: {Fore.RESET}').lower()
        usuario.establecerNombreUsuario(usu)
        psw = input(
            f'{Fore.GREEN}Password: {Fore.RESET}').lower().replace(" ", "")
        usuario.establecerPassword(psw)
        email = input(
            f'{Fore.GREEN}Email: {Fore.RESET}').lower().replace(" ", "")
        usuario.establecerEmail(email)
        # print(usuario.obtenerEmail())

        while True:
            if usuario.obtenerEmail() == 0:
                print(f'Correo invalido, intente de nuevo')
                input(f'\nPrecione una tecla para reintentar')
                MenuUsuario.registrarse(self)
            else:
                opcion = input(f'\nConfirmar registro? S/N: ').lower()

                while True:
                    if opcion == 's':
                        usuario.agregarUsuario(usuario.obtenerIdUsuario(),
                                               usuario.obtenerIdRol(),
                                               usuario.obtenerUsuario(),
                                               usuario.obtenerPassword(),
                                               usuario.obtenerEmail())
                        print(
                            f'\n{Fore.GREEN}Usuario registrado correctamente{Fore.RESET}')
                        print(f'''Seleccione una opcion
                                                        A: Agregar otro usuario
                                                        F: Finalizar la carga''')
                        volverACargar = input(f'>> ').lower()
                        if volverACargar == 'a':
                            MenuUsuario.registrarse(self)
                        elif volverACargar == 'f':
                            return tester.MenuOrganica.menuPrincial(self)
                    elif opcion == 'n':
                        print(f'Ha cancelado la carga del usuario.')
                        return tester.MenuOrganica.menuPrincial(self)

    def conectarse(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}CONECTARSE{Fore.RESET}')
        dataUsuario = usuarios.Usuario.cargarJson()

        usu = input(f'{Fore.GREEN}Nombre Usuario: {Fore.RESET}')
        psw = input(f'{Fore.GREEN}Password: {Fore.RESET}')
        for usuarioActual in dataUsuario['usuarios']:
            if usuarioActual['nombre_usuario'] == usu and usuarioActual['password'] == psw:
                return tester.MenuOrganica.menuPrincial(self, usuarioActual)

        print(f'Usuario no encontrado, intente de nuevo')
        input(f'\nPrecione una tecla para continuar')
        return MenuUsuario.conectarse(self)

    def verUsuarios():
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}VER USUARIOS{Fore.RESET}')
        usuariosLista = usuarios.Usuario.verUsuarios()
        for i, u in enumerate(usuariosLista, start=1):
            print(f'{i}: {Fore.GREEN}ID:{Fore.RESET}{u.obtenerIdUsuario()}, {Fore.GREEN}Nombre:{Fore.RESET} {u.obtenerUsuario()}')
        return input(f'\nPrecione una tecla para continuar')


# print(MenuUsuario.verUsuarios())
