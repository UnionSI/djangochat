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
            } else {
                alignMessage = 'align-self-start'
            }
            break;
        case 'Homologacion':
            if (userName == data.usuario) {
                alignMessage = 'align-self-start'
            } else {
                alignMessage = 'align-self-end'
            }
            break;
    }
    //const alignMessage = userName == data.username? 'align-self-end': 'align-self-start'
    document.querySelector('#chat-messages').innerHTML += (
        `<div class="${alignMessage} d-flex flex-column p-2 bg-white border rounded">
            <div>
            <small class="text-secondary">${formattedDate} -</small>
            <small class="text-secondary">${data.usuario}</small>
            </div>
            <small>${data.mensaje}</small>
        </div>`
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

document.querySelector('#chat-message-input').focus();

form = document.querySelector('#form-chat-submit')
form.addEventListener('submit', function(e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    globalSocket.send(JSON.stringify({
        'type': 'chat_message',
        'mensaje': message,
        'usuario': userName,
        'contacto': roomName,
        'telefono': phoneNumber,
        'integracion': integracion,
        'ambiente': ambiente
    }));

    console.log('mensaje enviado a la ws: ',{
        'type': 'chat_message',
        'mensaje': message,
        'usuario': userName,
        'contacto': roomName,
        'telefono': phoneNumber,
        'integracion': integracion,
        'ambiente': ambiente
    })

    messageInputDom.value = '';
});

function formatoFecha(date) {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const hours = date.getHours();
    let minutes = date.getMinutes();
    minutes = minutes < 10 ? "0" + minutes: minutes
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

function scrollAlFinal() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollAlFinal();