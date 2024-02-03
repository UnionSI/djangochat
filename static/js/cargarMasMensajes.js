import { manejarMensajeRecibido } from './manejarMensajeRecibido.js'

let loading = false;

async function cargarMasMensajes() {
    if (loading) {
        return;
    }

    let objDiv = document.getElementById("chat-messages");

    if (objDiv.scrollTop === 0 && objDiv.scrollHeight > objDiv.clientHeight) {
        loading = true;
        const alturaOriginal = objDiv.scrollHeight + 100

        // Obtener el número de la próxima página
        let nextPage = parseInt(objDiv.getAttribute('data-next-page')) || 2;

        // Realizar una solicitud AJAX al servidor para obtener más mensajes
        fetch(`ajax/${nextPage}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status == 'success') {
                data.mensajes.forEach(async dataMensaje => {
                    const elemento = await manejarMensajeRecibido(dataMensaje, false)
                    objDiv.scrollTop = elemento.scrollHeight - alturaOriginal
                })
    
                // Actualizar el número de la próxima página
                objDiv.setAttribute('data-next-page', nextPage + 1);
    
            } else {
                console.log(data.status)
                objDiv.removeEventListener('scroll', cargarMasMensajes);
            }
        })
        .catch(error => {
            console.error('Error al cargar más mensajes:', error);
        })
        .finally(() => {
            loading = false;
        });
    }
}

// Agregar el manejador de eventos al contenedor de mensajes
let objDiv = document.getElementById("chat-messages");
objDiv.addEventListener('scroll', cargarMasMensajes);