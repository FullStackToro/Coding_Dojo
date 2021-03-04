from django.db import models
import bcrypt
import re
from datetime import datetime
from time import gmtime, strftime


class UsuarioManager(models.Manager):
    def validacion_registro(self, postData):
        error = {}
        if not len(postData['fecha']):
            pass
        else:
            time = datetime.strptime(postData['fecha'], '%Y-%m-%d')
            now=datetime.now()
            var = datetime.strptime(f"{int(now.year) - 16}-{now.month}-{now.day}", '%Y-%m-%d')
            if time > datetime.now():
                error['net_1'] = f"La fecha no puede ser superior a {now.year}/{now.month}/{now.day}"
            elif time > var:
                error['edad'] = "El usuario debe tener al menos 16 años para poderse registrar."

        largo_data = [2, 2, 8]
        if(len(postData['nombre']) < largo_data[0]):
            error['nombre'] = f"El nombre debe tener al menos {largo_data[0]} caracteres"
        if len(postData['alias']) < largo_data[1]:
            error['alias'] = f"El alias debe tener al menos {largo_data[1]} caracteres"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern
            error['email'] = "La dirección de Email no válida"
        if len(postData['password']) < largo_data[2]:
            error['password'] = f"La password debe tener al menos {largo_data[2]} caracteres"
        if postData['password'] != postData['password_confirm']:
            error['password-confirm'] = f"Las contraseñas ingresadas no coinciden"
        if Usuario.objects.filter(cuenta__email__icontains=postData['email']):
            error['email_reviews'] = f"El correo {postData['email']} ya se encuentra en nuestros registros."

        return error

    def validacion_login(self, postData):
        error = {}
        try:
            user = Usuario.objects.get(cuenta__email=str(postData['login_email']))
            if bcrypt.checkpw(postData['login_password'].encode(), user.cuenta.password.encode()):
                return error
            else:
                error['password-revision'] = "La contraseña ingresada no es valida"
                return error
        except:
            error['login_email'] = f"{postData['login_email']} no se encuentra registrado"
            return error


    def password_hash(self, postData):
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return hash1

class Cuenta(models.Model):
    email = models.CharField(max_length=55)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id_cuenta_friends = models.ManyToManyField('login_app.Usuario', related_name="id_usuario_friends")

class Usuario(models.Model):
    name = models.CharField(max_length=55)
    alias = models.CharField(max_length=55)
    fNacimiento = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cuenta = models.ForeignKey(Cuenta, related_name='usuario', on_delete=models.CASCADE)
    objects = UsuarioManager()




