from mongoengine import *
from models.oficina import Oficina

class RegistrarVisitante(Document):
    nombreCompleto = StringField(required=True)
    correo = EmailField(required=True)
    oficina = ReferenceField(Oficina, required=True)

    meta = {'collection': 'registrarvisitante'}

    def __repr__(self):
        return f"<Ingreso: {self.nombreCompleto} ({self.oficina})>"


