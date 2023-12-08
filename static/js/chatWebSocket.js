const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const phoneNumber = JSON.parse(document.getElementById('json-phone-number').textContent);

const globalSocket = new WebSocket('wss://' + window.location.host + '/ws/global/');

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
            if (roomName == data.room) {
                handleMessageOnChat(data);
            }
            //UpdateMessageOnRoomsList(data);
            break;
        default:
            console.error('Unknown message type: ', data.type);
    }
    scrollToBottom()
};

function handleMessageOnChat(data) {
    const formattedDate = formatDate(new Date());
    const alignMessage = userName == data.username? 'align-self-end': 'align-self-start'
    document.querySelector('#chat-messages').innerHTML += (
        `<div class="${alignMessage} d-flex flex-column p-2 bg-white border rounded">
            <div>
            <small class="text-secondary">${formattedDate} -</small>
            <small class="text-secondary">${data.username}:</small>
            </div>
            <small>${data.message}</small>
        </div>`
    );
}

function UpdateMessageOnRoomsList(data) {
    const roomList = document.getElementById('room-list');
    const divRoom = document.getElementById(data.room);
    if (divRoom) {
        const date = new Date();
        divRoom.querySelector(".message-date").innerHTML = `${date.getHours()}:${date.getMinutes()}`;
        divRoom.querySelector(".message-content").innerHTML = data.message;
        roomList.insertBefore(divRoom, roomList.firstChild);
    }
}

document.querySelector('#chat-message-input').focus();

form = document.querySelector('#form-chat-submit')
form.addEventListener('submit', function(e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    console.log({
        'type': 'chat_message',
        'message': message,
        'username': userName,
        'room': roomName,
        'phone': phoneNumber
    })

    globalSocket.send(JSON.stringify({
        'type': 'chat_message',
        'message': message,
        'username': userName,
        'room': roomName,
        'phone': phoneNumber
    }));

    messageInputDom.value = '';

});

function formatDate(date) {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollToBottom();