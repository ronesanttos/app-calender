from mongoengine import Document, StringField, DateTimeField, EmailField,  ReferenceField, CASCADE  #type:ignore
from werkzeug.security import generate_password_hash #type:ignore

class User(Document):
    nome = StringField(required=True)
    email = EmailField(unique=True)
    password = StringField(required=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
class Evento(Document):
    nome = StringField(required=True)
    data_evento = DateTimeField()
    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    def __str__(self):
        return f"{self.nome} - {self.data_evento}"

