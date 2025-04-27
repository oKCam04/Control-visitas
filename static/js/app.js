
function agregarEntrada() {
    const url = "/Entradas/";
    const entrada = {
        NombreVisitante: document.getElementById('txtNombreVisitante').value,
        fecha: document.getElementById('txtFecha').value,
        oficina: document.getElementById('cbOficina').value,
        Estado: document.getElementById('cbEstado').value
    };

    fetch(url, {
        method: "POST",
        body: JSON.stringify(entrada),
        headers: {
            "Content-Type": "application/json",
        }
    })
    .then(respuesta => respuesta.json())
    .then(resultado => {
        if (resultado.estado) {
            location.href = "/EntradaAsistente/";
        } else {
            Swal.fire("Agregar Entrada", resultado.mensaje, "warning");
        }
    })
    .catch(error => {
        console.error(error);
    });
}

/**
* Eliminar una entrada por ID
* @param {string} id
*/
function deleteEntrada(id) {
    Swal.fire({
        title: "¿Está seguro de querer eliminar esta Entrada?",
        showDenyButton: true,
        confirmButtonText: "Sí",
        denyButtonText: "No"
    }).then((result) => {
        if (result.isConfirmed) {
            const entrada = {
                id: id
            };
            const url = "/Entradas/";
            fetch(url, {
                method: "DELETE",
                body: JSON.stringify(entrada),
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(respuesta => respuesta.json())
            .then(resultado => {
                if (resultado.estado) {
                    location.href = "/EntradaAsistente/";
                } else {
                    Swal.fire("Eliminar Entrada", resultado.mensaje, "warning");
                }
            })
            .catch(error => {
                console.error(error);
            });
        }
    });
}

function validarEntrada() {
    const nombre = document.getElementById('NombreVisitante').value.trim();
    const fecha = document.getElementById('fecha').value.trim();
    const oficina = document.getElementById('oficina').value;
    const estado = document.getElementById('Estado').value;

    if (!nombre || !fecha || !oficina || !estado) {
        return false;
    }

    return true;
}
function editarEntrada(id) {
    
    if (validarEntrada()) {
        const entrada = {
            id: id,
            NombreVisitante: document.getElementById('NombreVisitante').value,
            fecha: document.getElementById('fecha').value,
            oficina: document.getElementById('oficina').value,
            Estado: document.getElementById('Estado').value
        };

        
        fetch('/Entradas/', {
            method: 'PUT',
            body: JSON.stringify(entrada),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.estado) {
                location.href = "/EntradaAsistente/";  
            } else {
                swal.fire("Error", data.mensaje, "warning");
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        swal.fire("Editar Entrada", "Por favor, complete todos los campos correctamente.", "warning");
    }
}





/**
* Eliminar una oficina por ID
* @param {string} id
*/
function deleteOficina(id) {
    Swal.fire({
        title: "¿Está seguro de querer eliminar esta Oficina?",
        showDenyButton: true,
        confirmButtonText: "Sí",
        denyButtonText: "No"
    }).then((result) => {
        if (result.isConfirmed) {
            const oficina = {
                id: id
            };
            const url = "/Oficina/";

            fetch(url, {
                method: "DELETE",
                body: JSON.stringify(oficina),
                headers: {
                    "Content-Type": "application/json"
                }
            })
            .then(respuesta => respuesta.json())
            .then(resultado => {
                if (resultado.estado) {
                    const fila = document.getElementById('oficina-' + id);
                    if (fila) {
                        fila.remove();
                    }
                    Swal.fire("Éxito", "Oficina eliminada correctamente", "success");
                } else {
                    Swal.fire("Eliminar Oficina", resultado.mensaje, "warning");
                }
            })
            .catch(error => {
                console.error(error);
                Swal.fire("Error", "Hubo un problema al eliminar la oficina", "error");
            });
        }
    });
}



function agregarOficina() {
    const nombreOficina = document.getElementById('txtNombreOficina').value.trim();

    if (!nombreOficina) {
        Swal.fire('Error', 'El nombre de la oficina es obligatorio', 'warning');
        return;
    }

    const oficina = {
        nombreOficina: nombreOficina
    };

    fetch('/Oficina/', {
        method: 'POST',
        body: JSON.stringify(oficina),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.estado) {
            Swal.fire('Éxito', 'Oficina agregada correctamente', 'success').then(() => {
                window.location.href = '/listarOficina/';
            });
        } else {
            Swal.fire('Error', data.mensaje, 'warning');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        Swal.fire('Error', 'Hubo un problema al agregar la oficina', 'error');
    });
}

function agregarServidor() {
    
    const nombreCompleto = document.getElementById("txtNombreCompleto").value;
    const correo = document.getElementById("txtCorreo").value;
    const oficinaId = document.getElementById("cbOficina").value;

  
    if (!nombreCompleto || !correo || !oficinaId) {
        Swal.fire("Error", "Todos los campos son obligatorios", "error");
        return;
    }

    const servidor = {
        nombreCompleto: nombreCompleto,
        correo: correo,
        oficina: oficinaId  
    };

   
    fetch("/RegistrarServidor/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(servidor)
    })
    .then(response => response.json())
    .then(resultado => {
        if (resultado.estado) {
            
            Swal.fire("Éxito", resultado.mensaje, "success").then(() => {
                window.location.href = "/ListarServidores/";
            });
        } else {
           
            Swal.fire("Error", resultado.mensaje, "warning");
        }
    })
    .catch(error => {
        console.error("Error al agregar servidor:", error);
        Swal.fire("Error", "Hubo un problema al registrar el servidor.", "error");
    });
}


