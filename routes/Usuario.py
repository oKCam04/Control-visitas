from app import app 
from flask import Flask, request, render_template, session, jsonify, flash, redirect, url_for
from models.Usuario import Usuario
from models.oficina import Oficina
import os 
import yagmail
import threading
from dotenv import load_dotenv
import random
import string
load_dotenv()

@app.route("/Usuarios/",methods=["GET"])
def ListarUsuarios():
    try:
        mensaje=None 
        usuarios=Usuario.objects()
    except Exception as error:
        mensaje=str(error)

    return {"mensaje":mensaje, "Usuarios":usuarios}

@app.route("/Usuarios/", methods=['POST'])
def addUsuarios():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json(force=True)
            usuario = Usuario(**datos)
            usuario.save()
            estado = True
            mensaje = "Genero agregado correctamente"
        else:
            mensaje = "No permitido"
    except Exception as error:
        mensaje = str(error)

    return {"estado": estado, "mensaje": mensaje}


@app.route("/")
def login():
    return render_template("iniciarSesion.html")

@app.route("/iniciarSesion/", methods=["POST"])
def iniciarSesion():
    mensaje = None
    try:
        username = request.form['txtUser']
        password = request.form['txtPassword']

        usuario = Usuario.objects(usuario=username, contrasena=password).first()
        correo = os.environ.get("CORREO")
        clave = os.environ.get("ENVIAR_CORREO")

        if usuario:
            session['user'] = username
            session['user_name'] = usuario.nombreCompleto
            email = yagmail.SMTP(correo, clave, encoding="utf-8")
            asunto = "Ingreso al sistema"
            mensaje = f"Ha ingresado al aplicativo {usuario.nombreCompleto}" 
            thread = threading.Thread(target=enviarCorreo, args=(email, [usuario.email], asunto, mensaje))
            thread.start()

            # Redirigir según el tipo de usuario
            if usuario.tipo_usuario == "Asistente":
                return redirect(url_for('homeAsistente'))
            elif usuario.tipo_usuario == "Administrador":
                return redirect(url_for('homeAdmin'))
            else:
                flash("Tipo de usuario desconocido", "error")
                return redirect(url_for('iniciarSesion'))

        else:
            mensaje = "Credenciales incorrectas"

    except Exception as error:
        mensaje = str(error)

    return render_template("iniciarSesion.html", mensaje=mensaje)


def enviarCorreo(email=None, destinatario=None, asunto=None, mensaje=None):
   email.send(to=destinatario, subject=asunto, contents=mensaje)


@app.route("/registrarU/")
def registrarU():
    try:
        mensaje=None 
        oficina=Oficina.objects()
    except Exception as error:
        mensaje=str(error)
    return render_template("RegistrarUsuario.html", oficina=oficina)



@app.route("/registrarUser/", methods=["POST"])
def registrar_usuario():
    try:
        nombre_completo = request.form['txtNombre']
        email = request.form['txtEmail']
        oficina_id = request.form['txtOficina']
        tipo_usuario = request.form['cbTipoUsuario']
        oficina = Oficina.objects(id=oficina_id).first()

        if not oficina:
            flash("La oficina no existe", "error")
              

        contrasena = generar_contrasena()

        usuario_data = {
            "nombreCompleto": nombre_completo,
            "email": email,
            "oficina": oficina,
            "tipo_usuario": tipo_usuario,
            "usuario": email,  
            "contrasena": contrasena  
        }

        usuario = Usuario(**usuario_data)
        usuario.save()

        enviar_correo(email, contrasena)

        flash("Usuario registrado correctamente. Por favor, inicia sesión.", "success")

        return render_template('registrarUsuario.html')  

    except Exception as error:
        flash(f"Error al registrar el usuario: {str(error)}", "error")
    return render_template('registrarUsuario.html')
       


def generar_contrasena(longitud=8):
    """Generar una contraseña aleatoria."""
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(caracteres) for i in range(longitud))


def enviar_correo(email, contrasena):
    """Enviar correo usando Yagmail."""
    try:
        correo = os.environ.get("CORREO")
        clave = os.environ.get("ENVIAR_CORREO")
        yag = yagmail.SMTP(correo, clave, encoding="utf-8")
        asunto = "Bienvenido a la Plataforma"
        cuerpo = f"Hola, Tu usuario es: {email} Tu contraseña es: {contrasena} Saludos!"
        yag.send(to=email, subject=asunto, contents=cuerpo)
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

@app.route("/cerrarSesion/")
def cerrarSesion():
    session.clear()
    mensaje="sesion cerrada"
    return render_template("iniciarSesion.html", mensaje=mensaje)




