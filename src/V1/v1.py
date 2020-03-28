#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from servicioV1 import ServiceForecasting


service = ServiceForecasting()
app = Flask(__name__)

# ------------------ Servicio V1 ------------------------------------------------#
# Ruta para ver la predicción del servicio v1
@app.route('/servicio/v1/prediccion/<n>horas', methods = ['GET'])
def inicio(n):
	return jsonify(service.predict(n)),200

# Ruta que devuelve status OK
@app.route('/servicio/v1/status', methods = ['GET'])
def status():
	return jsonify(status="OK"),200

# Ruta para ver las rutas
@app.route('/', methods = ['GET'])
def index():
	return jsonify(status="OK",urlstatus="/servicio/v1/status",urlprediccion="/servicio/v1/prediccion/<n>horas"),200


if __name__ == '__main__':
	app.run(host='localhost', debug=True)