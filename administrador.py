import tester
import usuarios
from colorama import Fore


class Administrador:

    def verUsuarios():
        dataUsuarios = usuarios.Usuario.cargarJson()

        usuarioLista = []

        for usuario in dataUsuarios['usuarios']:
            usuario = usuarios.Usuario(
                usuario['id_usuario'],
                usuario['id_rol'],
                usuario['nombre_usuario'],
                usuario['password'],
                usuario['email'])
            usuarioLista.append(usuario)
        return usuarioLista

    def modificarUsuarios(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}MODIFICAR USUARIOS{Fore.RESET}')
        dataUsuario = usuarios.Usuario.cargarJson()

        buscarUsuario = input(
            f'{Fore.GREEN}Buscar usuario, "0" para cancelar: {Fore.RESET}')

        if buscarUsuario == '0':
            return

        buscar = buscarUsuario

        usuariosEncontrados = []

        for usuario in dataUsuario['usuarios']:
            encontrarUsuario = usuario['nombre_usuario']
            if all(palabra in encontrarUsuario for palabra in buscar):
                usuariosEncontrados.append(usuario)

        if not usuariosEncontrados:
            return f'{Fore.RED}No se encontraron usuarios con el nombre "{buscar}"{Fore.RESET}'

        print(f'{Fore.GREEN}Usuario encontrado{Fore.RESET}')
        for i, usuario in enumerate(usuariosEncontrados, start=1):
            print(f'{i}. Nombre: {usuario["nombre_usuario"]}')

        elegirI = int(f'{Fore.GREEN}Elegir usuario: {Fore.RESET}') - 1

        if elegirI < 0 or elegirI >= len(usuariosEncontrados):
            return f'{Fore.RED}Opcion invalida{Fore.RESET}'
        else:
            usuarioSeleccionado = usuariosEncontrados[elegirI]
            usuario = usuarios(usuarioSeleccionado['id_usuario'],
                               usuarioSeleccionado['id_rol'],
                               usuarioSeleccionado['nombre_usuario'],
                               usuarioSeleccionado['password'],
                               usuarioSeleccionado['email'])
            return usuario
