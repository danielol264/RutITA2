from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, id, usuario,contraseña):
        self.id=id
        self.usuario=usuario
        self.contraseña=contraseña
    @classmethod
    def generar_contraseña(self,contraseña):
        return generate_password_hash(contraseña)
    @classmethod
    def chechar_contraseña(self,contraseña_hasheada, contraseña):
        return check_password_hash( contraseña_hasheada, contraseña)