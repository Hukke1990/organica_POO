from flask import Flask, render_template, request, redirect, url_for
import menuProductos
import menuCliente
from datetime import datetime
import os
import platform

app = Flask(__name__)

def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
              "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)

    return messsage

def limpiarPantalla():  # limpiar la consola completa
    sistema_operativo = platform.system()
    if sistema_operativo == "Windows":
        os.system("cls")
    else:
        os.system("clear")

@app.route('/', methods=['GET', 'POST'])
def main():
    now = datetime.now()
    current_date = current_date_format(now)
    menu = {
        '1': 'Menu Clientes',
        '2': 'Menu Productos',
        '3': 'Menu Ventas',
        '4': 'Menu Proveedores'
    }
    if request.method == 'POST':
        opcion = request.form.get('opcion')
        if opcion == '1':
            return redirect(url_for('menu_clientes'))
        elif opcion == '2':
            return redirect(url_for('menu_productos'))
        # Aquí podrías agregar más opciones si lo necesitas
    return render_template('index.html', date=current_date, menu=menu)

@app.route('/clientes', methods=['GET', 'POST'])
def menu_clientes():
    if request.method == 'POST':
        # Aquí iría el código para agregar clientes
        menuCliente.MenuCliente.agregarClientes()
    # Aquí iría el código para ver clientes
    clientes = menuCliente.MenuCliente.verClientes()
    return render_template('clientes.html', clientes=clientes)

@app.route('/productos', methods=['GET', 'POST'])
def menu_productos():
    if request.method == 'POST':
        # Aquí iría el código para agregar productos
        menuProductos.MenuProductos.agregarProductos()
    # Aquí iría el código para ver productos
    productos = menuProductos.MenuProductos.verProductos()
    return render_template('productos.html', productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
