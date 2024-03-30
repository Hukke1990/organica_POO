import productos
import tester
from colorama import Fore


class MenuProductos:

    def obtenerControlStock(self):
        dataProductos = productos.Productos.cargarJson()

        productosNecesitanReponer = []

        for producto in dataProductos['productos']:
            nombreProducto = producto["nombre"]
            cantidadProducto = producto["cantidad_disponible"]

            stock = 25  # modifica la cantidad mínima de stock

            if stock >= cantidadProducto:
                productosNecesitanReponer.append(nombreProducto)

        if productosNecesitanReponer:
            resultado = f'{Fore.RED}Productos que necesitan reponer el stock:{Fore.RESET}\n'
            for producto in productosNecesitanReponer:
                resultado += f' {producto} {Fore.RED}necesita reponer el stock {Fore.RESET}\n'
        else:
            resultado = f'{Fore.GREEN}No hay productos que necesiten reponer el stock hoy{Fore.RESET}'

        return resultado

    def verProductos():
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}VER PRODUCTOS{Fore.RESET}')
        productoLista = productos.Productos.verProductos()
        for i, p in enumerate(productoLista, start=1):
            print((f'{i}: {Fore.GREEN}ID:{Fore.RESET} {p.obtenerIdProducto()}, {Fore.GREEN}Nombre:{Fore.RESET} {p.obtenerNombreProducto().capitalize()}, {Fore.GREEN}Proveedor:{Fore.RESET} {p.obtenerProveedor().capitalize()}, {Fore.GREEN}Precio:{Fore.RESET} {p.obtenerPrecioProducto()}'))
        return input(f'\nPrecione una tecla para continuar')

    def agregarProductos(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}AGREGAR PRODUCTOS{Fore.RESET}')
        productoNuevo = productos.Productos(0, "", "", 0, "", "", "", 0)
        productoNuevo.establecerIdProducto()
        nom = input(f'{Fore.GREEN}Nombre producto: ')
        productoNuevo.establecerNombreProducto(nom)
        desc = input(f'{Fore.GREEN}Descripcion producto: {Fore.RESET}')
        productoNuevo.establecerDescripcionProducto(desc)
        pre = input(f'{Fore.GREEN}Precio producto: {Fore.RESET}')
        productoNuevo.establecerPrecioProducto(pre)
        cat = input(f'{Fore.GREEN}Categoria producto: {Fore.RESET}')
        productoNuevo.establecerCategoriaProducto(cat)
        pro = input(f'{Fore.GREEN}Proveedor producto: {Fore.RESET}')
        productoNuevo.establecerProveedor(pro)
        productoNuevo.establecerFecha()
        cant = input(f'{Fore.GREEN}Cantidad disponible: {Fore.RESET}')
        productoNuevo.establecerCantidadDisponible(cant)

        while True:
            opcion = input(f'Confirmar producto S/N: ').lower()

            if opcion == 's':
                productoNuevo.agregarProductoCompleto(productoNuevo.obtenerNombreProducto(),
                                                      productoNuevo.obtenerDescripcionProducto(),
                                                      productoNuevo.obtenerPrecioProducto(),
                                                      productoNuevo.obtenerCategoriaProducto(),
                                                      productoNuevo.obtenerProveedor(),
                                                      productoNuevo.obtenerFechaJson(),
                                                      productoNuevo.obtenerCantidadDisponible())
                print(f'''Seleccione una opcion
                            A: agregar otro producto
                            F: Finalizar la carga''')
                volverACargar = input(f'>> ').lower()
                if volverACargar == 'a':
                    self.agregarProductos()
                elif volverACargar == 'f':
                    return
                else:
                    print(f'Opción invalida. Por favor, ingresa "a" o "f"')

            elif opcion == 'n':
                print(f'Ha cancelado la carga del producto.')
                return tester.MenuOrganica.menuPrincipal()
            else:
                print(f'Opción invalida. Por favor, ingresa "s" o "n"')

    def buscarProducto(self):
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}BUSCAR PRODUCTO{Fore.RESET}')
        productoBuscar = []

        # verifica que el cliente excista, de ser asi lo agrega a la lista ClienteBuscar
        buscarProducto = productos.Productos.buscarProducto()
        if buscarProducto is not None:
            productoBuscar.append(buscarProducto)

        tester.limpiarPantalla()
        print(f'{Fore.CYAN}PRODUCTO ENCONTRADO{Fore.RESET}')
        for p in productoBuscar:
            atributos = ['ID', 'Nombre', 'Descripcion', 'Precio', 'Categoria',
                         'Proveedor', 'Fecha ingreso', 'Cantidad disponible']
            metodos = [p.obtenerIdProducto, p.obtenerNombreProducto, p.obtenerDescripcionProducto, p.obtenerPrecioProducto,
                       p.obtenerCategoriaProducto, p.obtenerProveedor, p.obtenerFecha, p.obtenerCantidadDisponible]
            for atributo, metodo in zip(atributos, metodos):
                try:
                    print(f'{Fore.GREEN}{atributo}: {Fore.RESET}{metodo()}')
                except TypeError:
                    print(f'Error: {metodo} no es un método válido')

        while True:
            opcion = input(f'\nEditar producto? S/N: ').lower()

            if opcion == 's':
                MenuProductos.editarProductos(self, productoBuscar)
            elif opcion == 'n':
                return
            else:
                print(f'Opción invalida. Por favor, ingresa "s" o "n"')

    def modificarPrecio():
        tester.limpiarPantalla()
        print(f'{Fore.CYAN}MODIFICACION GENERAL DE PRECIOS{Fore.RESET}')
        nuevoPrecio = productos.Productos.modificarPrecio()

        for i in nuevoPrecio["productos"]:
            print(f'\n{Fore.GREEN}Producto:{Fore.RESET} {i["nombre"]}')
            print(f'{Fore.GREEN}Nuevo Precio:{Fore.RESET} {i["precio"]}$ ')
            print('{:->35}'.format(''))

        opcion = input(f'\nCargar el aumento? S/N: ').lower()

        while True:
            if opcion == 's':
                print(f'{Fore.GREEN}Precios modificados correctamente{Fore.RESET}')
                productos.Productos.guardarJson(dataProductos=nuevoPrecio)
                input(f'\nPrecione una tecla para continuar')
            elif opcion == 'n':
                return
            else:
                print(f'Opción invalida. Por favor, ingresa "s"" o "n"')
            break

    def editarProductos(self, productoBuscar):
        camposModificados = []

        while True:
            tester.limpiarPantalla()
            print(f'{Fore.CYAN}EDICION DE PRODUCTOS{Fore.RESET}')
            print(f'Datos producto')
            print('{:->35}'.format(''))

            for p in productoBuscar:
                atributos = ['ID', 'Nombre', 'Descripcion', 'Precio', 'Categoria',
                             'Proveedor', 'Fecha ingreso', 'Cantidad disponible']
                metodos = [p.obtenerIdProducto, p.obtenerNombreProducto, p.obtenerDescripcionProducto, p.obtenerPrecioProducto,
                           p.obtenerCategoriaProducto, p.obtenerProveedor, p.obtenerFecha, p.obtenerCantidadDisponible]
                for atributo, metodo in zip(atributos, metodos):
                    if atributo in camposModificados:
                        print(f'{Fore.CYAN}{atributo}: {Fore.RESET}{metodo()}')
                    else:
                        print(f'{Fore.GREEN}{atributo}: {Fore.RESET}{metodo()}')
            print('\n')

            opcionEdicion = {
                1: 'Editar nombre',
                2: 'Editar descripcion',
                3: 'Editar precio',
                4: 'Editar categoria',
                5: 'Editar proveedor',
                6: 'Editar fecha',
                7: 'Editar cantidad disponible',
                8: 'Guardar cambios',
                9: 'Eliminar producto',
                10: 'Volver al menu anterior'
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
                    p.establecerNombreProducto(nuevoNombre)
                    camposModificados.append('Nombre')
            elif opcion == 2:
                nuevaDescripcion = input(
                    f'Nueva descripcion, "c" para cancelar: ').lower()
                if nuevaDescripcion == 'c':
                    continue
                else:
                    p.establecerDescripcionProducto(nuevaDescripcion)
                    camposModificados.append('Descripcion')
            elif opcion == 3:
                nuevoPrecio = input(
                    f'Nueva precio, "c" para cancelar: ').lower()
                if nuevoPrecio == 'c':
                    continue
                else:
                    if p.establecerPrecioProducto(nuevoPrecio):
                        camposModificados.append('Precio')
                    else:
                        print(
                            f'\n{Fore.RED}debe ingresar un precio valido{Fore.RESET}')
                        input(f'precione ENTER para continuar')
            elif opcion == 4:
                nuevaCategoria = input(
                    f'Nueva categoria, "c" para cancelar: ').lower()
                if nuevaCategoria == 'c':
                    continue
                else:
                    p.establecerCategoriaProducto(nuevaCategoria)
                    camposModificados.append('Categoria')
            elif opcion == 5:
                nuevoProveedor = input(
                    f'Nuevo proveedor, "c" para cancelar: ').lower()
                if nuevoProveedor == 'c':
                    continue
                else:
                    p.establecerProveedor(nuevoPrecio)
                    camposModificados.append('Proveedor')
            elif opcion == 6:
                nuevaFecha = input(
                    f'Nueva fecha (ej: AAAA-MM-DD), "c" para cancelar: ').lower()
                if nuevaFecha == 'c':
                    continue
                else:
                    if p.establecerFechaProducto(nuevaFecha):
                        camposModificados.append('Fecha ingreso')
                    else:
                        print(f'\n{Fore.RED}Fecha invalida{Fore.RESET}')
                        input(f'precione ENTER para continuar')
                        continue
            elif opcion == 7:
                nuevaCantidadDisponible = input(
                    f'Nueva cantidad disponible, "c" para cancelar: ')
                if nuevaCantidadDisponible == 'c':
                    continue
                else:
                    if p.establecerCantidadDisponible(nuevaCantidadDisponible):
                        camposModificados.append('Cantidad disponible')
                    else:
                        print(
                            f'\n{Fore.RED}Debe ingresar solo numeros{Fore.RESET}')
                        input(f'precione ENTER para continuar')
                        continue
            elif opcion == 8:
                productos.Productos.editarProducto(p)
                print(f'\n{Fore.GREEN}Producto modificado{Fore.RESET}')
                input(f'precione ENTER para continuar')

            elif opcion == 9:
                productos.Productos.eliminiarProducto(p)
                print(f'{Fore.RED}Producto eliminado{Fore.RESET}')
                input(f'precione ENTER para continuar')

            elif opcion == 10:
                tester.MenuOrganica.menuProductos(self)


# print(MenuProductos.obtenerControlStock())
