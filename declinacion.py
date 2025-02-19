from flask import Flask, request, render_template, send_file
import pandas as pd
import numpy as np
import io

app = Flask(__name__)

def calcular_declinacion(azimuth, altura, latitud):
    """Calcula la declinación astronómica a partir de azimuth, altura y latitud."""
    azimuth_rad = np.radians(azimuth)
    altura_rad = np.radians(altura)
    latitud_rad = np.radians(latitud)
    
    declinacion_rad = np.arcsin(np.sin(latitud_rad) * np.sin(altura_rad) + np.cos(latitud_rad) * np.cos(altura_rad) * np.cos(azimuth_rad))
    return np.degrees(declinacion_rad)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        try:
            azimuth = float(request.form['azimuth'])
            altura = float(request.form['altura'])
            latitud = float(request.form['latitud'])
            resultado = calcular_declinacion(azimuth, altura, latitud)
        except ValueError:
            resultado = "Error: Ingrese valores numéricos válidos."
    return render_template('index.html', resultado=resultado)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No se subió ningún archivo."
    
    file = request.files['file']
    df = pd.read_csv(file)
    df["Declinacion"] = df.apply(lambda row: calcular_declinacion(row["Azimuth"], row["Altura"], row["Latitud"]), axis=1)
    
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='resultado.csv')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

