from django.shortcuts import render, HttpResponse, redirect
from .models import Usuario, Cuenta
from django.contrib import messages

def home(request):
    request.session['log_user']=0
    return render(request, 'index.html')

#Registro de Usuarios
def registrar(request):
    error = Usuario.objects.validacion_registro(request.POST)
    password = Usuario.objects.password_hash(request.POST)
    if len(error) > 0:
        for key, value in error.items():
            messages.error(request, value)
            print(key, value)
        return redirect('/')
    else:
        temp = Cuenta.objects.create(email=request.POST['email'], password=password)
        Usuario.objects.create(name=request.POST['nombre'], apellido=request.POST['apellido'], cuenta=temp)
    return redirect("/registrado")

def registrado(request):
    return render(request, 'success.html')

#Login de Usuarios
def login(request):
    error2=Usuario.objects.validacion_login(request.POST)
    if len(error2) > 0:
        print('ocurrio un error')
    else:
        request.session['log_user'] = request.POST['login_email']
        return redirect("/exito")
    return redirect('/')

def logeado(request):
    if request.session['log_user']!=0:
        return render(request, "login.html")
    else:
        return redirect('/')

#Desconectar
def logout(request):
    request.session['log_user'] = 0
    return redirect('/')
