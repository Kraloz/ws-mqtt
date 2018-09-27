# -*- coding: utf-8 -*-

# -Librería de eventos-
import eventlet
eventlet.monkey_patch()
# ---------------------
#   -Webserver-
from flask import Flask, render_template, jsonify
# ---------------------
#   -SocketIO-
from flask_socketio import SocketIO, emit
# ---------------------
#   -Mqtt- 
from flask_mqtt import Mqtt
# ---------------------
#  -Para variables de entorno-
from os import environ
from dotenv import load_dotenv, find_dotenv
# ---------------------
from models import db, ma, Sensor, SensorSchema
import json

__author__ = "Tomás Aprile"


# Traigo las variables de entorno
load_dotenv(find_dotenv())
# Instancia de Flask
app = Flask(__name__)


# Settings
app.config['SECRET_KEY'] =  environ.get('SECRET_KEY')
app.config['DEBUG'] = True if environ.get('DEBUG') == 'True' else False

# BD
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# MQTT
app.config['MQTT_BROKER_URL'] = environ.get('MQTT_BROKER_URL')
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = True if environ.get('MQTT_TLS_ENABLED') == 'True' else False


# SocketIO
DOMAIN = environ.get('DOMAIN')
ASYNC_MODE = environ.get('ASYNC_MODE')


# Otras Instancias
db.init_app(app)                                #DB
mqtt = Mqtt(app)                                #MQTT
socketio = SocketIO(app, async_mode=ASYNC_MODE) #SocketIO

""" Enrutamiento
"""
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/json")
def jason():
    return render_template("json.html", title="json")


""" SocketIO Listeners """
@socketio.on("connect")
def on_connect():
    print("Client connected!")
    socketio.emit("hola", {"hola": "quetalxd"})

@socketio.on("message")
def handle_message(message):
    print('received message: ' + message)


@socketio.on("selectAll")
def handle_selectAll():
    """ Returns ALL the sensors from the db """
    sensor = Sensor.query.all()
    
    sensor_schema = SensorSchema(many=True)

    output = sensor_schema.dump(sensor).data

    socketio.emit("respuestaSensores", {"sensores": output})


@socketio.on("updateValue")
def test_connect(json_data):
    #Defino el esquema
    schema = SensorSchema()
    # deserializo el json a mi esquema
    json_deseria = schema.loads(json_data, partial=True)
    # lo parseo a un obj de mi modelo
    obj_json = json_deseria.data
    # traigo un sensor
    sensor = Sensor.query.get(1)
    # cambio el valor del sensor por el valor que me llegó del json
    sensor.valor = obj_json.valor
    # commiteo los cambios
    db.session.commit()   
    # llamo a la función que le actualiza los datos a los clientes 
    handle_selectAll()


""" Mqtt Listeners """
mqtt.subscribe("/test") # Sub a /test

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode("utf-8","ignore")
    )
    try:
        json_str = data["payload"]
        
    except Exception as e:
        print(e)
    else:
        schema = SensorSchema()

        json_deserialized = schema.loads(json_str, many=True, partial=True)
        
        json_objs = json_deserialized.data

        for item in json_objs:
            sensor = Sensor.query.get(item.id)

            # cambio el valor del sensor por el valor que me llegó del json
            try:
                sensor.valor = item.valor
                # commiteo los cambios
                db.session.commit()
                handle_selectAll()
            except Exception as e:
                print(e)
                
        

# Inicializamos el servidor
if __name__ == '__main__':   
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True)