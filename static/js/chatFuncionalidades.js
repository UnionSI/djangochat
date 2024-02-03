const botonAdjuntar = document.querySelector('#attached-button')
const botonAgregarAdjunto = document.querySelector('#file-attached-button')
const botonBorrarAdjunto = document.querySelector('#delete-attached-button')
const adjuntos = document.querySelector('#file-attached')
const cantidadAdjuntos = document.querySelector('#amount-files')
const toastAdjuntos = document.querySelector('#toast-attached')
const enviarMensaje = document.querySelector('#chat-message-submit')

/* Toast Adjuntos */
const toastLiveExample = document.getElementById('liveToast')
const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)

// Abre la ventana de adjuntos
botonAgregarAdjunto.addEventListener('click', () => {
  adjuntos.click()
})

// Borra los archivos adjuntos
botonBorrarAdjunto.addEventListener('click', () => {
  adjuntos.value = '';
  cantidadAdjuntos.innerHTML = 'Sin archivos adjuntos'
  toastAdjuntos.innerHTML = 'Se eliminaron todos los adjuntos'
  toastBootstrap.show()
  botonAdjuntar.classList.add('btn-light')
  botonAdjuntar.classList.remove('btn-secondary')
})

// Borra los archivos adjuntos al enviar mensaje
enviarMensaje.addEventListener('click', () => {
  cantidadAdjuntos.innerHTML = 'Sin archivos adjuntos'
  botonAdjuntar.classList.add('btn-light')
  botonAdjuntar.classList.remove('btn-secondary')
})

// Informa la cantidad de adjuntos
adjuntos.addEventListener('change', () => {
    const numArchivos = adjuntos.files.length;
    console.log(numArchivos)
    cantidadAdjuntos.innerHTML = `Archivos adjuntos: ${numArchivos}`
    toastAdjuntos.innerHTML = `Archivos adjuntos: ${numArchivos}`
    toastBootstrap.show()
    botonAdjuntar.classList.remove('btn-light')
    botonAdjuntar.classList.add('btn-secondary')
  })

/* 
const emojiButton = document.querySelector('#emoji-button');
 */

const emojiButton = document.getElementById('emojiButton')
emojiButton.addEventListener('click', () => {
  var emojiContainer = document.getElementById('emojiContainer');

  if (emojiContainer.style.display === 'none') {
      emojiContainer.style.display = 'block';
  } else {
      emojiContainer.style.display = 'none';
  }
});

document.querySelector('emoji-picker')
  .addEventListener('emoji-click', event => {
    console.log(event.detail)
    const inputText = document.querySelector('#chat-message-input');
    inputText.value += event.detail.unicode
});

// Cierra el emoji-picker si se hace clic fuera de él
/* document.addEventListener('click', function(event) {
  var emojiContainer = document.getElementById('emojiContainer');
  var emojiButton = document.getElementById('emojiButton');

  if (event.target !== emojiButton && !emojiContainer.contains(event.target)) {
      emojiContainer.style.display = 'none';
  }
}); */
