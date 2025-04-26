from mongoengine import *
from models.oficina import Oficina

class Usuario(Document):
    nombreCompleto = StringField(required=True)
    email = EmailField(required=True, unique=True)
    oficina = ReferenceField(Oficina, required=True)
    tipo_usuario = StringField(choices=['Asistente', 'Administrador'], required=True) 
    usuario = StringField(required=True, unique=True)
    contrasena = StringField(required=True)
    meta = {'collection': 'usuarios'}

    def __repr__(self):
        return f"<Usuario: {self.nombreCompleto} ({self.tipo_usuario})>"
