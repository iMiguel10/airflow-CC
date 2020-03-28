#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from servicioV2 import ServiceForecasting


service = ServiceForecasting()
app = Flask(__name__)

# ------------------ Servicio V2 ------------------------------------------------#
# Ruta para ver la predicción del servicio v2
@app.route('/servicio/v2/prediccion/24horas', methods = ['GET'])
def predict24h():
    data,cod = service.predict(24)
    return data,cod

# Ruta para ver la predicción del servicio v2
@app.route('/servicio/v2/prediccion/48horas', methods = ['GET'])
def predict48h():
    data,cod = service.predict(48)
    return jsonify(data),cod

    # Ruta para ver la predicción del servicio v2
@app.route('/servicio/v2/prediccion/72horas', methods = ['GET'])
def predict72h():
    data,cod = service.predict(72)
    return jsonify(data),cod

# Ruta que devuelve status OK
@app.route('/servicio/v2/status', methods = ['GET'])
def status():
	return jsonify(status="OK"),200

# Ruta para ver las rutas
@app.route('/', methods = ['GET'])
def index():
	return jsonify(status="OK",urlstatus="/servicio/v2/status",urlprediccion=["/servicio/v2/prediccion/24horas","/servicio/v2/prediccion/48horas","/servicio/v2/prediccion/72horas"]),200

if __name__ == '__main__':
	app.run(host='localhost', debug=True)