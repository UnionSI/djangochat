import { manejarMensajeRecibido } from './manejarMensajeRecibido.js'
import { responderMensajes } from './chatWebSocket.js'


let cajaChat = document.getElementById("chat-messages");
let loading = false;

async function cargarMasMensajes() {
    if (loading) {
        return;
    }

    let cajaChat = document.getElementById("chat-messages");
    const ambiente = JSON.parse(document.getElementById('json-ambiente').textContent);
    const usuariosData = document.getElementById('usuarios-data').dataset.usuarios;
    const usuariosArray = JSON.parse(usuariosData.replace(/'/g, "\""));

    if (cajaChat.scrollTop === 0 && cajaChat.scrollHeight > cajaChat.clientHeight) {
        loading = true;
        const alturaOriginal = cajaChat.scrollHeight + 100

        // Obtener el número de la próxima página
        let nextPage = parseInt(cajaChat.getAttribute('data-next-page')) || 2;

        // Realizar una solicitud AJAX al servidor para obtener más mensajes
        fetch(`cargar-mas-mensajes/${nextPage}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status == 'success') {
                data.mensajes.forEach(async dataMensaje => {
                    const elemento = await manejarMensajeRecibido(dataMensaje, ambiente, cajaChat, false, usuariosArray)
                    cajaChat.scrollTop = elemento.scrollHeight - alturaOriginal
                })
    
                // Actualizar el número de la próxima página
                cajaChat.setAttribute('data-next-page', nextPage + 1);
    
            } else {
                console.log(data.status)
                cajaChat.removeEventListener('scroll', cargarMasMensajes);
            }
        })
        .catch(error => {
            console.error('Error al cargar más mensajes:', error);
        })
        .finally(() => {
            loading = false;
            responderMensajes()
        });
    }
}

// Agregar el manejador de eventos al contenedor de mensajes
cajaChat.addEventListener('scroll', cargarMasMensajes);