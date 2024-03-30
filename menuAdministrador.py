import usuarios
import menuUsuario
import tester
from colorama import Fore


class MenuAdministrador:
    def verUsuarios():
        # tester.limpiarPantalla()
        print(f'{Fore.CYAN}USUARIOS{Fore.RESET}')
        usuarioLista = MenuAdministrador.verUsuarios()

        for i, usuario in enumerate(usuarioLista, start=1):
            print(str(i) + ('{:->35}'.format('')))
            print(f'{Fore.GREEN}ID: {Fore.RESET}{usuario["id_usuario"]}')
            print(f'{Fore.GREEN}Rol: {Fore.RESET}{usuario["id_rol"]}')
            print(
                f'{Fore.GREEN}Usuario: {Fore.RESET}{usuario["nombre_usuario"]}')
            print(f'{Fore.GREEN}Password: {Fore.RESET}{usuario["password"]}')
            print(f'{Fore.GREEN}Email: {Fore.RESET}{usuario["email"]}')

        input(f'\nPrecione una tecla para continuar')


MenuAdministrador.verUsuarios()
