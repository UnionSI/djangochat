import { manejarMensajeRecibido } from './manejarMensajeRecibido.js'

const cajaChat = document.getElementById("chat-messages")
const form = document.querySelector('#form-chat-submit')

form.addEventListener('submit', (e) => {
    e.preventDefault()

    const mensajeInputDom = document.querySelector('#chat-message-input')
    const mensaje = mensajeInputDom.value

    if (mensaje) {
        
        // Dibujar mensaje del usuario 
        const mensajeUsuario = {
            'contacto': '',
            'mensaje': mensaje,
            'usuario': 'Usuario',
            'url_adjunto': '',
            'mencion': ''
        }
        manejarMensajeRecibido(mensajeUsuario, 'Homologacion', cajaChat, true, [''])

        // Dibujar mensaje del bot
        fetch(`/bot/test/bot_responde/?mensaje=${mensaje}`)
        .then(response => response.json())
        .then(response => {
            const data = response.data[0]
            manejarMensajeRecibido(data, 'Homologacion', cajaChat, true, ['ChatBot'])
        })
        .catch(error => {
            console.error('Error:', error)
        })

        mensajeInputDom.value = ''
    }
})