const roomName = JSON.parse(document.getElementById('json-roomname').textContent);
const userName = JSON.parse(document.getElementById('json-username').textContent);
const urlWS = 'ws://' + window.location.host + '/ws/' + roomName + '/'
const chatSocket = new WebSocket(urlWS);

console.log(roomName)
console.log(userName)
console.log(urlWS)

chatSocket.onclose = function(e) {
    console.log('onclose')
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    const now = new Date();
    const day = now.getDate();
    const month = now.getMonth() + 1;
    const year = now.getFullYear();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const formattedDate = `${day}/${month}/${year} ${hours}:${minutes}`;

    switch (data.type) {
        case 'chat_message':
            document.querySelector('#chat-messages').innerHTML += (
            `<div class="{% if user.is_staff %} align-self-end {% else %} align-self-start {% endif %} d-flex flex-column p-2 bg-white border rounded">
                <div>
                <small class="text-secondary">${formattedDate} -</small>
                <small class="text-secondary">${data.username}:</small>
                </div>
                <small>${data.message}</small>
            </div>`
            );
            break;
        case 'room_update':
            console.log(data.room_slug, data.last_message, data.room)
            divRoom = document.querySelector(`#${data.room}`)
            divRoom.querySelector(".message-date").innerHTML = formattedDate
            divRoom.querySelector(".message-content").innerHTML = data.last_message
        default:
            console.error('Unknown message type: ', data.type)
    }
    scrollToBottom();
};

document.querySelector('#chat-message-input').focus();

form = document.querySelector('#form-chat-submit')
form.addEventListener('submit', function(e) {
    e.preventDefault()

    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;

    console.log({
        'message': message,
        'username': userName,
        'room': roomName
    })

    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'room': roomName
    }));

    messageInputDom.value = '';

    //return false
    });


function scrollToBottom() {
    let objDiv = document.getElementById("chat-messages");
    objDiv.scrollTop = objDiv.scrollHeight;
}

scrollToBottom();