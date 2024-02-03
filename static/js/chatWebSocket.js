const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const usuariosData = document.getElementById('usuarios-data').dataset.usuarios;
const usuariosArray = JSON.parse(usuariosData.replace(/'/g, "\""));
const phoneNumber = JSON.parse(document.getElementById('json-phone-number').textContent);
const integracion = JSON.parse(document.getElementById('json-integracion').textContent);
const ambiente = JSON.parse(document.getElementById('json-ambiente').textContent);
const debug = JSON.parse(document.getElementById('json-debug').textContent);

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

form = document.querySelector('#form-chat-submit')
form.addEventListener('submit', function(e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input')
    const message = messageInputDom.value;
    const inputFilesDom = document.getElementById('file-attached')
    const files = inputFilesDom.files;

    if (message || files.length > 0) {
        const json_data = {
            'type': 'chat_message',
            'mensaje': message,
            'usuario': userName,
            'contacto': roomName,
            'telefono': phoneNumber,
            'integracion': integracion,
            'ambiente': ambiente,
            'media': ''
        }

        if (files.length > 0) {
            let filesValid = true
            const maxSize = 10 * 1024 * 1024; // 10 MB en bytes
            for (var i = 0; i < files.length; i++) {
                const fileSize = files[i].size; // Tamaño en bytes
                filesValid =  maxSize >= fileSize
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
                console.log('El archivo adjunto pesa más de 10mb')
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