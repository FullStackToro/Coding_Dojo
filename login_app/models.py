from django.db import models
import re
import bcrypt



class UsuarioManager(models.Manager):
    def validacion_registro(self, postData):
        error = {}
        largo_data = [2, 2, 8]
        if(len(postData['nombre']) < largo_data[0]):
            error['nombre'] = f"El nombre debe tener al menos {largo_data[0]} caracteres"
        if len(postData['apellido']) < largo_data[1]:
            error['apellido'] = f"El apellido debe tener al menos {largo_data[1]} caracteres"
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
        user = Usuario.objects.get(cuenta__email=str(postData['login_email']))
        if user:
            if bcrypt.checkpw(postData['login_password'].encode(), user.cuenta.password.encode()):
                return error
            else:
                error['password-revision'] = "La contraseña ingresada no es valida"
        else:
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

class Usuario(models.Model):
    name = models.CharField(max_length=55)
    apellido = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cuenta = models.ForeignKey(Cuenta, related_name='usuario', on_delete=models.CASCADE)
    objects=UsuarioManager()
# Create your models here.



