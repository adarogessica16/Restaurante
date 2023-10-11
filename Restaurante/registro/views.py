from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
import bcrypt

from registro.utils.decoradores import login_requerido


def registro(request):
    if request.method == 'GET':

        if 'usuario' in request.session:
            messages.warning(request,"Ya estás registrado.")
            return redirect("/")


        context = {}
        return render(request, 'registro/registro.html', context)

    if request.method == 'POST':
        # Llama a la función validar del UsuarioManager
        errores = Usuario.objects.validar(request.POST)

        if errores:
            # Si hay errores de validación, muestra un mensaje de error y vuelve al formulario
            for error in errores.values():
                messages.error(request, error)
            return redirect("/registro/registro")

        pass_encriptada = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(f"la contraseña '{request.POST['password']}' con bcrypt quedo en: {pass_encriptada}")

        user = Usuario.objects.create(
            nombre = request.POST['nombre'],
            apellido = request.POST['apellido'],
            email = request.POST['email'],
            tipo_usuario=request.POST['tipo_usuario'],
            password = pass_encriptada,
        )


        usuario_session = {
            'id' : user.id,
            'nombre' : user.nombre + ' ' + user.apellido,
            'email' : user.email,
            'tipo_usuario':user.tipo_usuario
        }

        print(usuario_session)
        request.session['usuario'] = usuario_session

        messages.success(request, "Usuario creado exitosamente.")
        return redirect("/registro/login")

def login(request):
    if request.method == 'GET':

        if 'usuario' in request.session:
            messages.warning(request,"Ya iniciaste Sesion")
            return redirect("inicio:inicio")

        context = {}
        return render(request, 'registro/login.html', context)

    if request.method == 'POST':
        usuarios = Usuario.objects.filter(email=request.POST['email']) 
        if usuarios: 
            usuario = usuarios[0] 
            print(usuario)

            if bcrypt.checkpw(request.POST['password'].encode(), usuario.password.encode()):

                usuario_session = {
                    'id' : usuario.id,
                    'nombre' : usuario.nombre + ' ' + usuario.apellido,
                    'email' : usuario.email,
                    'tipo_usuario':usuario.tipo_usuario
                }

                print('El usuario de la sesion', usuario_session)
                request.session['usuario'] = usuario_session
                messages.success(request, "Haz iniciado sesion!")
                return redirect('inicio:inicio')
            else:
                messages.error(request, "La contraseña o el correo no coinciden")
                return redirect("/registro/login/")

        else:
            messages.error(request,"El correo o la contraseña indicado no existe")
            return redirect("/registro/login/")
        
        

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']

    return redirect("/registro/login/")

