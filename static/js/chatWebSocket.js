const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const usuariosData = document.getElementById('usuarios-data').dataset.usuarios;
const usuariosArray = JSON.parse(usuariosData.replace(/'/g, "\""));
const phoneNumber = JSON.parse(document.getElementById('json-phone-number').textContent);
const integracion = JSON.parse(document.getElementById('json-integracion').textContent);
const ambiente = JSON.parse(document.getElementById('json-ambiente').textContent);
const debug = JSON.parse(document.getElementById('json-debug').textContent);
const sector = document.getElementById('sector')
const sectorTarea = document.getElementById('sector-tarea')
const form = document.querySelector('#form-chat-submit')
const responderMensajes = document.querySelectorAll('.responder-mensaje')

protocolo = debug == true ? 'ws' : 'wss'
const globalSocket = new WebSocket(protocolo + '://' + window.location.host + '/ws/global/');

globalSocket.onopen = function(e) {
    console.log('Global WebSocket opened');
};

globalSocket.onclose = function(e) {
    console.log('Global WebSocket closed');
    manejarErrores('Error de comunicación', 'Es necesario recargar la página para reestablecer la conexión')
};

globalSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    console.log('Mensaje recibido:', data);

    switch (data.type) {
        case 'chat_message':
            if (roomName == data.contacto) {
                manejarMensajeRecibido(data, true);
            }
            //actualizarListaContactos(data);
            break;
        case 'message_error':
            if (roomName == data.contacto && userName == data.usuario ) {
                manejarErrores('Error al enviar mensaje', data.mensaje)
            }
            break;
        case 'sector_change':
            sector.innerText = data.sector
            sectorTarea.innerHTML = data.sector_tarea
            break;
        default:
            console.error('Unknown message type: ', data.type);
    }
    scrollAlFinal()
};


function actualizarListaContactos(data) {
    const roomList = document.getElementById('room-list');
    const divRoom = document.getElementById(data.contacto);
    if (divRoom) {
        const date = new Date();
        divRoom.querySelector(".message-date").innerHTML = `${date.getHours()}:${date.getMinutes()}`;
        divRoom.querySelector(".message-content").innerHTML = data.mensaje;
        roomList.insertBefore(divRoom, roomList.firstChild);
    }
}

function manejarErrores(titulo, mensaje) {
    const boxError = document.querySelector('#box-error')
    const modalTitle = boxError.querySelector('.modal-title')
    const modalBody = boxError.querySelector('.modal-body')
    modalTitle.innerHTML = titulo
    modalBody.innerHTML = mensaje
    boxError.classList.remove('d-none')
    const closeButtons = document.querySelectorAll('[data-bs-close="modal"]')
    closeButtons.forEach(closeButton => {
        closeButton.addEventListener('click', () => {
            boxError.classList.add('d-none')
        })
    })
}

function scrollAlFinal() {
    let objDiv = document.getElementById("chat-messages");
    setTimeout(() => {
        objDiv.scrollTop = objDiv.scrollHeight
      }, "250")
}

responderMensajes.forEach(responderMensaje => {
    responderMensaje.addEventListener('click', (e) => {
        // Verificar si ya hay mensajes citados y eliminarlos
        const mensajeCitados = form.parentElement.querySelectorAll('.caja-citar-chat')
        if (mensajeCitados.length > 0) {
            mensajeCitados.forEach(mensajeCitado => mensajeCitado.remove())
        }
        // Crear el mensaje citado
        const cajaMensaje = e.target.closest('.caja-mensaje-chat');
        const cabeceraMensaje = cajaMensaje.querySelector('.mensaje-cabecera').textContent
        const contenidoMensaje = cajaMensaje.querySelector('.mensaje-contenido').textContent
        let adjuntoMensaje = cajaMensaje.querySelector('.mensaje-adjunto')
        if (adjuntoMensaje.children.length > 0) {
            adjuntoMensaje = `
                <div class="mt-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-text" viewBox="0 0 16 16">
                        <path d="M5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zM5 9.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5"/>
                        <path d="M9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.5zm0 1v2A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
                    </svg>
                    <small>Archivo citado</small>
                </div>
            `
        } else {
            adjuntoMensaje = ''
        }
        const htmlMensaje = `
            <div class="d-flex flex-column">
                <small class="fw-medium">${cabeceraMensaje}</small>
                <small>${contenidoMensaje}</small>
                ${adjuntoMensaje}
            </div>
            <button type="button" class="btn btn-close btn-sm position-absolute top-0 end-0 mt-1 me-1" aria-label="Close"></button>
        `
        const div = document.createElement('div')
        div.classList.add('caja-citar-chat', 'bg-body-secondary', 'border', 'rounded', 'p-2', 'mb-2', 'position-relative')
        div.innerHTML = htmlMensaje
        form.parentElement.insertBefore(div, form);
        // Botón para cancelar mensaje citado
        form.parentElement.querySelector('.btn-close').addEventListener('click', () => div.remove())
    })
})

form.addEventListener('submit', (e) => {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input')
    const message = messageInputDom.value;
    const inputFilesDom = document.getElementById('file-attached')
    const files = inputFilesDom.files;
    const mentioned = document.getElementById('chat-mentioned')

    if (message || files.length > 0) {
        const json_data = {
            'type': 'chat_message',
            'mensaje': message,
            'usuario': userName,
            'contacto': roomName,
            'telefono': phoneNumber,
            'integracion': integracion,
            'ambiente': ambiente,
            'media': '',
            'mencion': mentioned
        }

        if (files.length > 0) {
            let filesValid = true
            const maxSizeMb = 16
            const maxSizeB = maxSizeMb * 1024 * 1024; // 10 MB en bytes
            for (var i = 0; i < files.length; i++) {
                const fileSize = files[i].size; // Tamaño en bytes
                filesValid =  maxSizeB >= fileSize
            }
            if (filesValid) {
                for (var i = 0; i < files.length; i++) {
                    let reader = new FileReader();
                    reader.onload = function (e) {
                        const base64Data = e.target.result;
                        json_data['media'] = base64Data
                        globalSocket.send(JSON.stringify(json_data))
                    }
                    reader.readAsDataURL(files[i]);
                }
            } else {
                console.log(`El archivo adjunto pesa más de ${maxSizeMb} MB`)
                manejarErrores('Error al enviar el archivo', `El archivo adjunto pesa más de ${maxSizeMb} MB`)
            }
        } else {
            globalSocket.send(JSON.stringify(json_data));
        }

        messageInputDom.value = '';
        inputFilesDom.value = ''
    }
});

window.addEventListener('load', function() {
    document.querySelector('#chat-message-input').focus();
    scrollAlFinal();
})