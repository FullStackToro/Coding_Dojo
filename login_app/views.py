from django.shortcuts import render, HttpResponse, redirect
from .models import Usuario, Cuenta
from django.contrib import messages


def home(request):
 #   request.session['log_name'] = ""
  #  request.session['log_alias'] = ""
   # request.session['log_email'] = ""
   # request.session['log_user'] = 0
    return render(request, 'index.html')

#Registro de Usuarios
def registrar(request):
    error = Usuario.objects.validacion_registro(request.POST)
    if len(error) > 0:
        request.session['mensaje'] = 0
        for key, value in error.items():
            request.session['error_registro'] = messages.error(request, value)
            print(key, value)
        return redirect('/')
    else:
        password = Usuario.objects.password_hash(request.POST)
        temp = Cuenta.objects.create(email=request.POST['email'], password=password)
        Usuario.objects.create(name=request.POST['nombre'], alias=request.POST['alias'], fNacimiento=request.POST['fecha'], cuenta=temp)
    return redirect("/registrado")

def registrado(request):
    return render(request, 'registro_success.html')

#Login de Usuarios
def login(request):
    error=Usuario.objects.validacion_login(request.POST)
    if len(error) > 0:
        request.session['mensaje'] = 1
        for key, value in error.items():
            request.session['error_login'] = messages.error(request, value)
            print(key, value)
        return redirect('/')
    else:
        request.session['log_user'] = request.POST['login_email']
        users=Usuario.objects.get(cuenta__email__icontains=request.POST['login_email'])
        request.session['log_name']=f"{users.name}"
        request.session['log_alias'] = f"{users.alias}"
        request.session['log_email'] = f"{users.cuenta.email}"
        request.session['log_id'] = f"{users.cuenta.id}"
        print(Cuenta.objects.get(email=request.POST['login_email']).id)
        return redirect(f"/friends")

def logout(request):
    print('Deslogeado')
    request.session.flush()
    return redirect('/')

def friend(request):

    temp=Usuario.objects.all().exclude(id=request.session['log_id'])
    u1 = Usuario.objects.get(id=request.session['log_id'])
    for user in u1.cuenta.id_cuenta_friends.all():
        temp=temp.exclude(id=user.id)
    context={
        'friend': u1.cuenta.id_cuenta_friends.all(),
        'not_friend': temp
    }
    return render(request, "friends.html",context)

def add_friend(request, _id):
    u1=Usuario.objects.get(id=request.session['log_id'])
    u2 = Usuario.objects.get(id=_id)
    u1.cuenta.id_cuenta_friends.add(u2)
    u2.cuenta.id_cuenta_friends.add(u1)
    for user in u1.cuenta.id_cuenta_friends.all():
        print(user.name)
    return redirect("/friends")

def delete_friend(request, _id):
    print('entro', _id)
    u1 = Usuario.objects.get(id=request.session['log_id'])
    u2 = Usuario.objects.get(id=_id)
    u1.cuenta.id_cuenta_friends.remove(u2)
    u2.cuenta.id_cuenta_friends.remove(u1)
    return redirect("/friends")


def user(request, _id):
    user=Usuario.objects.get(id=_id)
    context={
        'user': user
    }
    return render(request, "perfil.html",context)
