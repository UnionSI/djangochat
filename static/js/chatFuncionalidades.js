const botonAdjuntar = document.querySelector('#attached-button')
const botonAgregarAdjunto = document.querySelector('#file-attached-button')
const botonBorrarAdjunto = document.querySelector('#delete-attached-button')
const adjuntos = document.querySelector('#file-attached')
const cantidadAdjuntos = document.querySelector('#amount-files')
const toastAdjuntos = document.querySelector('#toast-attached')
const enviarMensaje = document.querySelector('#chat-message-submit')
const claseBotonAdjuntoOn = 'btn-success'

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
  cantidadAdjuntos.innerHTML = 'Archivos adjuntos: 0'
  toastAdjuntos.innerHTML = 'Se eliminaron todos los adjuntos'
  toastBootstrap.show()
  botonAdjuntar.classList.add('btn-light')
  botonAdjuntar.classList.remove(claseBotonAdjuntoOn)
  const nombreAdjuntos = document.querySelectorAll('.nombre-archivos')
  nombreAdjuntos.forEach(adjunto => {adjunto.remove()})
})

// Borra los archivos adjuntos al enviar mensaje
enviarMensaje.addEventListener('click', () => {
  cantidadAdjuntos.innerHTML = 'Archivos adjuntos: 0'
  const nombreAdjuntos = document.querySelectorAll('.nombre-archivos')
  nombreAdjuntos.forEach(adjunto => {adjunto.remove()})
  botonAdjuntar.classList.add('btn-light')
  botonAdjuntar.classList.remove(claseBotonAdjuntoOn)
})

const informarCantidadAdjuntos = () => {
  const numArchivos = adjuntos.files.length;
  cantidadAdjuntos.innerHTML = `Archivos adjuntos: ${numArchivos}`
  toastAdjuntos.innerHTML = `Archivos adjuntos: ${numArchivos}`
  toastBootstrap.show()
  if (numArchivos > 0) {
    botonAdjuntar.classList.remove('btn-light')
    botonAdjuntar.classList.add(claseBotonAdjuntoOn)
  } else {
    botonAdjuntar.classList.add('btn-light')
    botonAdjuntar.classList.remove(claseBotonAdjuntoOn)
  }
} 

// Informa la cantidad de adjuntos
adjuntos.addEventListener('change', () => {
    informarCantidadAdjuntos()
    
    /*
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x text-danger" viewBox="0 0 16 16">
    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
    </svg>
    */

    Array.from(adjuntos.files).forEach(adjunto => {
      const archivoAdjunto = `
          <li class="nombre-archivos" data-adjunto="${adjunto.name}">
              <button type="button" class="dropdown-item">
                  • ${adjunto.name}
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x text-danger" viewBox="0 0 16 16" style="margin-bottom: 3px">
                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708"/>
                  </svg>
              </button>
          </li>
      `;
      cantidadAdjuntos.parentNode.insertAdjacentHTML('beforeend', archivoAdjunto);
    })

    const listaAdjuntos = document.querySelectorAll(".nombre-archivos")
    listaAdjuntos.forEach(liAdjunto => liAdjunto.addEventListener('click', () => {
        // Eliminar el adjunto del input
        const nombreAdjunto = liAdjunto.getAttribute('data-adjunto');
        const nuevosArchivos = Array.from(adjuntos.files).filter(adjunto => adjunto.name !== nombreAdjunto);
        // Crear un nuevo objeto FileList
        const nuevoFileList = new DataTransfer();
        nuevosArchivos.forEach(adjunto => nuevoFileList.items.add(adjunto));

        // Asignar el nuevo FileList al input de archivos
        adjuntos.files = nuevoFileList.files;

        // Eliminar de la lista
        liAdjunto.remove();

        informarCantidadAdjuntos()
    }))

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
