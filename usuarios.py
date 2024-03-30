import random
from email_validator import validate_email, EmailNotValidError
import os
import json
from colorama import Fore


class Usuario:

    def __init__(self, idUsu, idRol, usu, psw, email):
        self.__idUsuario = idUsu
        self.__idRol = "usuario"
        self.__usuario = usu
        self.__password = psw
        self.__email = email

    # <<COMANDOS>>
    def establecerIdUsuario(self):
        self.__idUsuario = 'U00' + str(random.randint(10, 90))
        return self.__idUsuario

    def establecerIdRol(self, idRol):
        self.__idRol = idRol

    def establecerNombreUsuario(self, usu):
        # usu = input(f'Nombre de usuario: ')
        self.__usuario = usu

    def establecerPassword(self, psw):
        # psw = input(f'Password: ')
        self.__password = psw

    def establecerEmail(self, email):
        while True:
            self.__email = email
            try:
                # Validar el correo electrónico
                validate_email(email)
                # El correo electrónico es válido, almacenarlo en el atributo __email
                self.__email = email
                return True
            except EmailNotValidError:
                # El correo electrónico no es válido
                # print(f'Formato correo invalido, intente nuevamente!')
                self.__email = 0
                return False

    def agregarUsuario(self, idUsu, idRol, usu, psw, email):
        dataUsuario = {'usuarios': []}
        if os.path.exists('usuarios.json') and os.path.getsize('usuarios.json') > 0:
            dataUsuario = Usuario.cargarJson()

        if not idUsu or not usu or not psw or not email:
            print(f'Todos los campos son obligatorios')
            return

        usuarioExiste = any(u['nombre_usuario'] == usu.lower() and
                            u['email'] == email.replace(" ", "") for u in dataUsuario['usuarios'])

        if usuarioExiste:
            print(f'Este usuario ya se encuentra registrado')
            return

        dataUsuario['usuarios'].append({'id_usuario': idUsu,
                                        'id_rol': idRol,
                                        'nombre_usuario': usu,
                                        'password': psw,
                                        'email': email})

        Usuario.guardarJson(dataUsuario)
        # print(f'Usuario registrado correctamente')

    def buscarUsuario(self):
        dataUsuario = Usuario.cargarJson()

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

        elegirI = int(input(f'{Fore.GREEN}Elegir usuario: {Fore.RESET}')) - 1

        if elegirI < 0 or elegirI >= len(usuariosEncontrados):
            return f'{Fore.RED}Opcion invalida{Fore.RESET}'
        else:
            usuarioSeleccionado = usuariosEncontrados[elegirI]
            usuario = Usuario(usuarioSeleccionado['id_usuario'],
                              usuarioSeleccionado['id_rol'],
                              usuarioSeleccionado['nombre_usuario'],
                              usuarioSeleccionado['password'],
                              usuarioSeleccionado['email'])
            return usuario

    # <<CONSULTAS>>

    def obtenerIdUsuario(self):
        return self.__idUsuario

    def obtenerIdRol(self):
        return self.__idRol

    def obtenerUsuario(self):
        return self.__usuario

    def obtenerPassword(self):
        return self.__password

    def obtenerEmail(self):
        return self.__email

    def verUsuarios():
        dataUsuarios = Usuario.cargarJson()

        usuarioLista = []

        for usuario in dataUsuarios['usuarios']:
            usuario = Usuario(usuario['id_usuario'],
                              usuario['id_rol'],
                              usuario['nombre_usuario'],
                              usuario['password'],
                              usuario['email'])
            usuarioLista.append(usuario)
        return usuarioLista

    # MANEJO ARCHIVO JSON
    def cargarJson():
        with open('usuarios.json', 'r') as archivoUsuarios:
            dataUsuarios = json.load(archivoUsuarios)
            return dataUsuarios

    def guardarJson(dataUsuarios):
        with open('usuarios.json', 'w') as archivoUsuarios:
            json.dump(dataUsuarios, archivoUsuarios, indent=4)

    def __str__(self):
        return f'''Usuario:
                ID: {self.obtenerIdUsuario()}
                ID Rol: {self.obtenerIdRol()}
                Usuario: {self.obtenerUsuario()}
                Password: {self.obtenerPassword()}
                Email: {self.obtenerEmail()}'''


'''c = Usuario(0, "", "", "", "")

print(Usuario.obtenerIdRol(c))'''
