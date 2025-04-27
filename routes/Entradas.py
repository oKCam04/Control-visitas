from app import app
from flask import Flask, request, render_template, session
from models.Entradas import Entradas
from models.oficina import Oficina


@app.route("/Entradas/", methods=["GET"])
def ListarEntradas():
    try:
        mensaje = None
        entradas = Entradas.objects()
    except Exception as error:
        mensaje = str(error)

    return {"mensaje": mensaje, "Entradas": entradas}

@app.route("/Entradas/", methods=['POST'])
def addEntradas():
    try:
        mensaje = None
        estado = False
        if request.method == 'POST':
            datos = request.get_json(force=True)
            entradas = Entradas(**datos)
            entradas.save()
            estado = True
            mensaje = "Entrada agregada correctamente"
        else:
            mensaje = "No permitido"
    except Exception as error:
        mensaje = str(error)

    return {"estado": estado, "mensaje": mensaje}

@app.route("/Entradas/", methods=['PUT'])
def updateEntrada():
    try:
        mensaje = None
        estado = False
        if request.method == 'PUT': 
            datos = request.get_json(force=True)

            
            entrada = Entradas.objects(id=datos['id']).first()

            if entrada:  
                
                entrada.NombreVisitante = datos['NombreVisitante']
                entrada.fecha = datos['fecha']
                entrada.Estado = datos['Estado']

                oficina = Oficina.objects(id=datos['oficina']).first()
                if oficina:
                    entrada.oficina = oficina 
                else:
                    mensaje = "No se actualizó la oficina, porque no es válida."

                
                entrada.save()

                mensaje = "Entrada actualizada correctamente."
                estado = True
            else:
                mensaje = "Entrada no encontrada."
        else:
            mensaje = "Método no permitido."

    except Exception as error:
        
        mensaje = str(error)

   
    return {"estado": estado, "mensaje": mensaje}




@app.route("/Entradas/", methods=['DELETE'])
def deleteEntradas():
    try:
        mensaje = None
        estado = False
        datos = request.get_json(force=True)
        id = datos.get("id")
        entradas = Entradas.objects(id=id).first()
        if entradas:
            entradas.delete()
            estado = True
            mensaje = "Entrada eliminada correctamente"
        else:
            mensaje = "Entrada no encontrada"
    except Exception as error:
        mensaje = str(error)

    return {"estado": estado, "mensaje": mensaje}

# contenido admin


@app.route("/Entrada/", methods=["GET"])
def getEntradas():
    if "user" in session:
        try:
            mensaje = None
            entradas = Entradas.objects()
            oficina = Oficina.objects()
        except Exception as error:
            mensaje = str(error)
        return render_template("ListarEntradasA.html", mensaje=mensaje, entradas=entradas, oficina=oficina)
    else:
        mensaje = "Debe ingresar primero"
        return render_template("iniciarSesion.html", mensaje=mensaje)

@app.route("/HomeAdmin/", methods=["GET"])
def homeAdmin():
    if "user" in session:
        return render_template("contenidoAdmin.html")
    else:
        mensaje = "Debe ingresar primero"
        return render_template("iniciarSesion.html", mensaje=mensaje)

#contenido asistente
@app.route("/EntradaAsistente/", methods=["GET"])
def getEntradasAsistente():
    if "user" in session:
        try:
            mensaje = None
            entradas = Entradas.objects()
            oficina = Oficina.objects()
        except Exception as error:
            mensaje = str(error)
        return render_template("ListarEntradasS.html", mensaje=mensaje, entradas=entradas, oficina=oficina)
    else:
        mensaje = "Debe ingresar primero"
        return render_template("iniciarSesion.html", mensaje=mensaje)

@app.route("/EntradaAgregarAsistente/", methods=["GET"])
def getEntradasAgregarAsistente():
    if "user" in session:
        try:
            mensaje = None
            entradas = Entradas.objects()
            oficina = Oficina.objects()
        except Exception as error:
            mensaje = str(error)
        return render_template("AgregarEntradas.html", mensaje=mensaje, oficina=oficina, entradas=entradas)
    else:
        mensaje = "Debe ingresar primero"
        return render_template("iniciarSesion.html", mensaje=mensaje)

@app.route("/editarEntradaAsistente/<id>", methods=["GET"])
def editarEntrada(id):
    if "user" in session:
        try:
            entrada = Entradas.objects(id=id).first()
            oficina = Oficina.objects()
            return render_template("EditarEntradas.html", entrada=entrada, oficina=oficina)
        except Exception as error:
            return str(error)
    else:
        mensaje = "Debe ingresar primero"
        return render_template("iniciarSesion.html", mensaje=mensaje)


