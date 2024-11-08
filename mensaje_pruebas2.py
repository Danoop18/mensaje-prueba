from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import pywhatkit as kit

app = Flask(__name__)

# Ruta para la página principal


@app.route('/')
def index():
    return render_template('index.html')

# Ruta para manejar las pruebas


@app.route('/update', methods=['POST'])
def update_pruebas():
    pruebas = pd.read_csv('pruebas.csv', delimiter=',', encoding='utf-8')
    nt_pruebas = 0
    total = {}

    # Obtener datos del formulario
    prueba_seleccionadas = request.form.getlist('pruebas[]')

    for prueba in prueba_seleccionadas:
        cantidad = int(request.form[f'cantidad_{prueba.upper()}'])
        nt_pruebas += cantidad
        pruebas.loc[pruebas.Pruebas == prueba.upper(), 'Total'] -= cantidad
        total[prueba.upper()] = cantidad

    pruebas.to_csv('pruebas.csv', index=None)

    # Obtener la hora de envío seleccionada por el usuario
    hora_envio = request.form['hora_envio']
    hora, minuto = map(int, hora_envio.split(':'))

    # Enviar mensaje por WhatsApp
    numero_telefono = "+527861326775"
    mensaje = f"""
    Hola, actualización de las pruebas:
    Hubo {nt_pruebas} prueba(s) {', '.join([f'{j} {i}' for i, j in total.items()])}.
    Por tanto, hasta hoy nos quedan:
    {pruebas.Total[0]} DUO | {pruebas.Total[1]} SQ | {pruebas.Total[2]} Influenza | {pruebas.Total[3]} ABBOTT"""

    # Enviar mensaje a la hora seleccionada
    kit.sendwhatmsg(numero_telefono, mensaje, hora, minuto)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
