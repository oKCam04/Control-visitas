from app import app 
from flask import Flask, request, render_template, session 
from models.Usuario import Usuario
import os 
import yagmail
import threading
from dotenv import load_dotenv

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

@app.route("/iniciarSesion/",methods=["POST"])
def iniciarSesion():
    mensaje=None
    try:
            username = request.form['txtUser']
            password = request.form['txtPassword']

            usuario=Usuario.objects(usuario=username,password=password).first()
            correo=os.environ.get("CORREO")
            clave=os.environ.get("ENVIAR_CORREO")
            if usuario:
                session['user']=username
                session['user_name']=f"{usuario.nombres} {usuario.apellidos}"
                email= yagmail.SMTP(correo,clave, encoding="utf-8")
                asunto="Ingreso al sistema"
                mensaje=f"ha ingresado al aplicativo {usuario.nombres} {usuario.apellidos}"
                thread=threading.Thread(target=enviarCorreo, args=(email, [usuario.correo], asunto,mensaje))
                thread.start()
                return render_template("contenido.html")
            else:
                mensaje="credenciales incorrectas"
    except Exception as error:
        mensaje=str(error)

    return render_template("iniciarSesion.html", mensaje=mensaje)

def enviarCorreo(email=None, destinatario=None, asunto=None, mensaje=None):
   email.send(to=destinatario, subject=asunto, contents=mensaje)


@app.route("/registrarU/")
def registrarU():
    return render_template("registrarUsuario.html")
