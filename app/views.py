from app import app
from flask import render_template, request, redirect, url_for, flash
import csv

ficheromovimientos = 'data/movimientos.txt'


@app.route('/')
def index():
    #leer movimientos
    fMovimientos = open(ficheromovimientos, "r")
    csvreader = csv.reader(fMovimientos, delimiter=',', quotechar='"')
    movements = []
    for movimiento in csvreader: 
        movements.append(movimiento)

    #enviar movimientos a index.html
    return render_template('index.html', movimientos=movements)

@app.route('/nuevacompra', methods=['GET', 'POST'])
def compra():
    print(request.method)
    if request.method == 'GET':
        return render_template('nuevacompra.html')
    else:
        msg = validar(request.values)
        if msg != True:
            return render_template('nuevacompra.html', errores=msg)

        fMovimientos = open(ficheromovimientos, "a+")
        precioUnitario = float(request.values['cantidadPagada'])/float(request.values['cantidadComprada'])
        registro = '{},"{}",{},{},{},{},{}\n'.format(request.values['fecha'], 
                    request.values['concepto'], 
                    request.values['monedaComprada'], 
                    request.values['cantidadComprada'], 
                    request.values['monedaPagada'], 
                    request.values['cantidadPagada'], 
                    precioUnitario)
        fMovimientos.write(registro)
        fMovimientos.close()
        return redirect(url_for('index'))

def validar(values):
    errores = []
    if values['fecha'] == '':
        errores.append('Debe informar la fecha')
    
    if values['concepto'] == '':
        errores.append('Debe informar el concepto')

    if values['cantidadComprada'] == '':
        errores.append('Debe informar la cantidad comprada')

    if values['cantidadPagada'] == '':
        errores.append('Debe informar la cantidad pagada')   

    if len(errores) == 0:
        return True
    else:
        return errores    

@app.route('/skeleton.css')
def skeleton():
    return 'Hola, skeleton'