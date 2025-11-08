from mongoengine import Document, StringField, DateTimeField  #type:ignore

class Evento(Document):
    nome = StringField(required=True)
    data_evento = DateTimeField()

    def __str__(self):
        return f"{self.nome} - {self.data_evento}"
