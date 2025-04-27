from app import app
from flask import Flask, request, render_template, session
from models.RegistrarVisitante import RegistrarVisitante
from models.oficina import Oficina



@app.route("/RegistrarServidor/", methods=["GET"])
def ListarVisitantes():
    try:
        mensaje = None
        visitantes = RegistrarVisitante.objects()
    except Exception as error:
        mensaje = str(error)

    return {"mensaje": mensaje, "Visitantes": visitantes}

@app.route("/RegistrarServidor/", methods=['POST'])
def addServidor():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos= request.get_json(force=True)
            oficina=Oficina.objects(id=datos['oficina']).first()
            if oficina:
                datos['oficina']=oficina
                visitante=RegistrarVisitante(**datos)
                visitante.save()
                estado = True
                mensaje = "Servidor agregado correctamente"
        else:
            mensaje = "Método no permitido"
    except Exception as error:
        mensaje = str(error)

    return {"estado": estado, "mensaje": mensaje}







# contenido asistente

@app.route("/ListarServidores/", methods=["GET"])
def ListarServidores():
    if "user" in session:
        try:
            mensaje = None
            servidores = RegistrarVisitante.objects() 
            oficinas = Oficina.objects() 
        except Exception as error:
            mensaje = str(error)
        return render_template("ListarServidores.html", Servidores=servidores, oficinas=oficinas)
    else:
        mensaje = "Debe ingresar primero"
        return render_template("iniciarSesion.html", mensaje=mensaje)

@app.route("/RegistrarVisitante/", methods=["GET"])
def RegistrarServidor():
    if "user" in session:
        try:
            mensaje = None
            visitantes = RegistrarVisitante.objects()
            oficinas = Oficina.objects()
        except Exception as error:
            mensaje = str(error)
        return render_template("AgregarServidor.html", Visitantes=visitantes, Oficinas=oficinas)
    else:
        mensaje = "Debe ingresar primero"
        return render_template("iniciarSesion.html", mensaje=mensaje)


    
