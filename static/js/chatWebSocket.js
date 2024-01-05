const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
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
                manejarMensajeRecibido(data);
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

function manejarMensajeRecibido(data) {
    const formattedDate = formatoFecha(new Date());
    let alignMessage;

    switch (ambiente) {
        case 'Produccion':
            if (userName == data.usuario) {
                alignMessage = 'align-self-end'
                alignThumbnail = 'flex-row-reverse'
                bgColor = 'bg-union'
                textColor = 'text-white-50'
            } else {
                alignMessage = 'align-self-start'
                alignThumbnail = 'flex-row'
                bgColor = 'bg-white'
                textColor = 'text-secondary'
            }
            break;
        case 'Homologacion':
            if (userName == data.usuario) {
                alignMessage = 'align-self-start'
                alignThumbnail = 'flex-row'
                bgColor = 'bg-white'
                textColor = 'text-secondary'
            } else {
                alignMessage = 'align-self-end'
                alignThumbnail = 'flex-row-reverse'
                bgColor = 'bg-union'
                textColor = 'text-white-50'
            }
            break;
    }

    const url_adjunto = data.url_adjunto? `<div><img src="${data.url_adjunto}" alt="" class="mt-1" style="max-width: 330px; max-height: 330px;"></div>`: '';

    //const alignMessage = userName == data.username? 'align-self-end': 'align-self-start'
    document.querySelector('#chat-messages').innerHTML += (
        /*
        `<div class="${alignMessage} d-flex flex-column p-2 bg-white border rounded">
            <div>
            <small class="text-secondary">${formattedDate} -</small>
            <small class="text-secondary">${data.usuario}</small>
            </div>
            <small>${data.mensaje}</small>
        </div>`
        */
       `
       <div style="max-width: 60%;" class="${alignMessage} d-flex flex-column">
            <div class="d-flex ${alignThumbnail} gap-1 ">
            <img src="/static/img/logo.png" alt="ameport_logo" width="24" height="24" class="mt-1 rounded-circle">
                <div class="${bgColor} caja-mensaje-chat">
                    <div>
                        <small class="${textColor}">${formattedDate} -</small>
                        <small class="${textColor}">${data.usuario}</small>
                    </div>
                    ${url_adjunto}
                    <small>${data.mensaje}</small>
                </div>
            </div>
        </div>
       `
    );
}

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

document.querySelector('#chat-message-input').focus();

form = document.querySelector('#form-chat-submit')
form.addEventListener('submit', function(e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input')
    const message = messageInputDom.value;
    const files = document.getElementById('file-attached').files;

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
                    console.log(json_data)
                }
                reader.readAsDataURL(files[i]);
            }
        } else {
            console.log('El archivo adjunto pesa más de 10mb')
        }
    } else {
        globalSocket.send(JSON.stringify(json_data));
    }

    /*
    for (var i = 0; i < files.length; i++) {
      var reader = new FileReader();
      reader.onload = function (e) {
        var base64Data = e.target.result;
        // Aquí puedes enviar base64Data al servidor
        console.log('Imagen en base64:', base64Data);
      };
      reader.readAsDataURL(files[i]);
    }*/

    messageInputDom.value = '';
});

function formatoFecha(date) {
    const day = addZero(date.getDate());
    const month = addZero(date.getMonth() + 1);
    const year = date.getFullYear();
    const hours = addZero(date.getHours());
    let minutes = addZero(date.getMinutes());
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

function addZero(number) {
    return number < 10 ? "0" + number: number
}

function scrollAlFinal() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

window.addEventListener('load', function() {
    scrollAlFinal();
})