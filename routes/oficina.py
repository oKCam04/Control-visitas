from app import app
from flask import Flask, request, render_template, session
from models.oficina import Oficina

@app.route("/Oficina/", methods=["GET"])
def ListarOficina():
    try:
        mensaje = None
        oficina = Oficina.objects()
    except Exception as error:
        mensaje = str(error)

    return {"mensaje": mensaje, "Oficina": oficina}

@app.route("/Oficina/", methods=['POST'])
def addOficina():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json(force=True)
            oficina = Oficina(**datos)
            oficina.save()
            estado = True
            mensaje = "Oficina agregada correctamente"
        else:
            mensaje = "No permitido"
    except Exception as error:
        mensaje = str(error)

    return {"estado": estado, "mensaje": mensaje}

@app.route("/Oficina/", methods=['DELETE'])
def deleteOficina():
    try:
        mensaje = None
        estado = False
        if request.method == 'DELETE':  
            datos = request.get_json(force=True)
            oficina = Oficina.objects(id=datos['id']).first()  
            if oficina:
                oficina.delete()  # Eliminar oficina
                estado = True
                mensaje = "Oficina eliminada correctamente"
            else:
                mensaje = "No se encontró la oficina"
        else:
            mensaje = "Método no permitido"
    except Exception as error:
        mensaje = str(error)

    return {"estado": estado, "mensaje": mensaje}

# contenido asistente
@app.route("/HomeAsistente/")
def homeAsistente():
    return render_template("contenidoAsistente.html")

@app.route("/listarOficina/", methods=["GET"])
def ltsOficina():
    try:
        mensaje = None
        oficina = Oficina.objects()  
    except Exception as error:
        mensaje = str(error)

    return render_template("ListarOficinasS.html", oficina=oficina)  

@app.route("/AgregarOficinaAsistente/")
def AgregarOficina():
    return render_template("AgregarOficina.html")
