# -*- coding: utf-8 -*-

#   -Webserver-
from flask import Flask
# ---------------------
# -Extensión ORM para flask -
from flask_sqlalchemy import SQLAlchemy
# ---------------------
#  Object (de)Serializer 
from flask_marshmallow import Marshmallow, Schema
# ---------------------
#  -Para variables de entorno-
from os import environ
from dotenv import load_dotenv, find_dotenv
# ---------------------


__author__ = "Tomás Aprile"


# Traigo las variables de entorno
load_dotenv(find_dotenv())
# Instancio para el modelo
app = Flask(__name__)


# Settings
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# ORMs
db = SQLAlchemy(app)
ma = Marshmallow(app)


""" Modelo de tabla de BD
"""
class Sensor(db.Model):
    __tablename__ = "sensores"
    """ Representación de los campos
    """
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(45), unique=False, nullable=True)
    # tipo_sens = Column(Enum(TipoSensores))
    valor = db.Column(db.Integer, unique=False, nullable=True)

    def as_dict(self):    
        return {"id": self.id, "descripcion": self.descripcion, "valor": self.valor}
       
    def __repr__(self):
        return "<Sensor : {}, {}, {}>".format(self.id, self.descripcion, self.valor)


""" Esquemas de tabla de la BD
"""
class SensorSchema(ma.ModelSchema):
    class Meta:
        model = Sensor
