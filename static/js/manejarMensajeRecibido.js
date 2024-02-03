export async function manejarMensajeRecibido(data, colocarAlFinal=true) {
    const formattedDate = data.fecha_hora? data.fecha_hora: formatoFecha(new Date());
    let alignMessage, alignThumbnail, bgColor, textColor, bgSecondaryColor

    switch (ambiente) {
        case 'Produccion':
            //if (userName == data.usuario) {
            if (usuariosArray.includes(data.usuario)) {
                alignMessage = 'align-self-end'
                alignThumbnail = 'flex-row-reverse'
                bgColor = 'bg-union'
                textColor = 'text-white-50'
                bgSecondaryColor = '#ffffff20'
            } else {
                alignMessage = 'align-self-start'
                alignThumbnail = 'flex-row'
                bgColor = 'bg-white'
                textColor = 'text-secondary'
                bgSecondaryColor = '#00000020'
            }
            break;
        case 'Homologacion':
            //if (userName == data.usuario) {
            if (usuariosArray.includes(data.usuario)) {
                alignMessage = 'align-self-start'
                alignThumbnail = 'flex-row'
                bgColor = 'bg-white'
                textColor = 'text-secondary'
                bgSecondaryColor = '#00000020'
            } else {
                alignMessage = 'align-self-end'
                alignThumbnail = 'flex-row-reverse'
                bgColor = 'bg-union'
                textColor = 'text-white-50'
                bgSecondaryColor = '#ffffff20'
            }
            break;
    }

    let adjunto = null
    if (data.url_adjunto.includes('.')) {
        const formatosImagenes = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tiff', 'tif']
        const formatosAudio = ['mp3', 'ogg', 'acc', 'wav', 'oga']
        const extension = data.url_adjunto.substring(data.url_adjunto.lastIndexOf('.') + 1);
        if (formatosImagenes.includes(extension)) {
            adjunto = `
                <div>
                    <a href="${data.url_adjunto}" target="_blank">    
                        <img src="${data.url_adjunto}" alt="" class="mt-1" style="max-width: 330px; max-height: 330px;" onerror="manejarArchivoEliminadoDer(this)">
                    </a>
                </div>
            `
        } else if (formatosAudio.includes(extension)) {
            adjunto = `
                <div>
                    <audio controls class="mt-1">
                        <source src="${data.url_adjunto}" type>
                            El navegador no soporta el tipo de formato del audio
                    </audio>
                </div>
            `
        } else {
            const nombre_archivo = data.url_adjunto.substring(data.url_adjunto.lastIndexOf('/') + 1);
            const peso = await obtenerPesoArchivo(data.url_adjunto)
            adjunto = `
                <div>
                    <a href="${data.url_adjunto}" class="d-flex justify-content-center align-items-center ${textColor} text-decoration-none rounded-3 my-1 p-2 gap-1" style="background-color: ${bgSecondaryColor};" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" fill="currentColor" class="bi bi-file-earmark-arrow-down-fill" viewBox="0 0 16 16">
                            <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1m-1 4v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 11.293V7.5a.5.5 0 0 1 1 0"/>
                        </svg>
                        <div>
                            <p class="mb-0">${nombre_archivo}</p>
                            <small>Tamaño: ${peso.toFixed(2)} KB</small>
                        </div>
                    </a>
                </div>
            `
        }
    } else {
        adjunto = ''
    }
    
    const mensajeConEspacios = data.mensaje.replaceAll('\n', '<br>')
    const html = `
        <div style="max-width: 60%;" class="${alignMessage} d-flex flex-column">
            <div class="d-flex ${alignThumbnail} gap-1 ">
            <img src="/static/img/logo.png" alt="ameport_logo" width="24" height="24" class="mt-1 rounded-circle">
                <div class="${bgColor} caja-mensaje-chat">
                    <div>
                        <small class="${textColor}">${formattedDate} -</small>
                        <small class="${textColor}">${data.usuario}</small>
                    </div>
                    ${adjunto}
                    <small>${mensajeConEspacios}</small>
                </div>
            </div>
        </div>
    `
    const cajaChat = document.querySelector('#chat-messages')
    if (colocarAlFinal) {
        cajaChat.innerHTML += html
    } else {
        cajaChat.insertAdjacentHTML('afterbegin', html)
    }
    return cajaChat
}

async function obtenerPesoArchivo(url) {
    return fetch(url, {
        method: 'HEAD'
    })
    .then(response => {
        const contentLengthHeader = response.headers.get('Content-Length');
        if (contentLengthHeader) {
            const tamanioEnBytes = parseInt(contentLengthHeader, 10);
            const tamanioEnKB = tamanioEnBytes / 1024;
            return tamanioEnKB;
        } else {
            throw new Error('No se pudo obtener el tamaño del archivo.');
        }
    })
    .catch(error => {
        console.error('Error al obtener el tamaño del archivo:', error);
    });
}

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