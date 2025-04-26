from mongoengine import *

class Oficina(Document):
    nombreOficina = StringField(required=True, unique=True)
    
    def _repr_(self):
        return self.nombreOficina