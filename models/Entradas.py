from mongoengine import *
from models.oficina import Oficina

class Entradas(Document):
    NombreVisitante = StringField( required=True)
    fecha = StringField(max_length=9, required=True)
    oficina = ReferenceField(Oficina, required=True)
    Estado = StringField(choices=['Activo', 'Inactivo'], required=True)

    def __repr__(self):
        return f"<Entradas: {self.NombreVisitante} ({self.oficina})>"
