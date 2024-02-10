export async function manejarMensajeRecibido(data='', ambiente='Homologacion', cajaChat, colocarAlFinal=true, usuariosArray=[]) {
    const formattedDate = data.fecha_hora? data.fecha_hora: formatoFecha(new Date());
    let alignMessage, alignThumbnail, bgColor, textColor, bgSecondaryColor, bgColorMentioned, side

    switch (ambiente) {
        case 'Produccion':
            //if (userName == data.usuario) {
            if (usuariosArray.includes(data.usuario)) {
                alignMessage = 'align-self-end'
                alignThumbnail = 'flex-row-reverse'
                bgColor = 'bg-union'
                bgColorMentioned = 'bg-union-light'
                textColor = 'text-white-50'
                bgSecondaryColor = '#ffffff20'
                side = 'right'
            } else {
                alignMessage = 'align-self-start'
                alignThumbnail = 'flex-row'
                bgColor = 'bg-white'
                bgColorMentioned = 'bg-body-secondary'
                textColor = 'text-secondary'
                bgSecondaryColor = '#00000020'
                side = 'left'
            }
            break;
        case 'Homologacion':
            //if (userName == data.usuario) {
            if (usuariosArray.includes(data.usuario)) {
                alignMessage = 'align-self-start'
                alignThumbnail = 'flex-row'
                bgColor = 'bg-white'
                bgColorMentioned = 'bg-body-secondary'
                textColor = 'text-secondary'
                bgSecondaryColor = '#00000020'
                side = 'left'
            } else {
                alignMessage = 'align-self-end'
                alignThumbnail = 'flex-row-reverse'
                bgColor = 'bg-union'
                bgColorMentioned = 'bg-union-light'
                textColor = 'text-white-50'
                bgSecondaryColor = '#ffffff20'
                side = 'right'
            }
            break;
    }

    let mensajeCitado = null
    if (data.mencion) {
        //let encontrado = false
        //const existeMensaje = chequearMensajeExistente(data['contacto_id'], data['mencion'])
        /*
        while (!encontrado) {
            console.log('--- start --')
            console.log('data.mencion:', data.mencion)
            console.log('está el elemento?', cajaMensaje)
            encontrado = cajaMensaje ? true : false
            
        }/*
        /* 
        const = cajaMensaje = document.getElementById(data.mencion);
        const cabeceraMensaje = cajaMensaje.querySelector('.mensaje-cabecera').textContent
        const contenidoMensaje = cajaMensaje.querySelector('.mensaje-contenido').textContent
        let adjuntoMensaje = cajaMensaje.querySelector('.mensaje-adjunto')
        if (adjuntoMensaje.children.length > 0) {
            */

        const cabeceraMensaje = `${data.mencion.fecha_hora} - ${data.mencion.usuario}`
        const contenidoMensaje = data.mencion.mensaje
        let adjuntoMensaje = data.mencion.url_adjunto

        if (adjuntoMensaje) {
            adjuntoMensaje = `
                <div class="mt-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-text" viewBox="0 0 16 16">
                        <path d="M5.5 7a.5.5 0 0 0 0 1h5a.5.5 0 0 0 0-1zM5 9.5a.5.5 0 0 1 .5-.5h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m0 2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 0 1h-2a.5.5 0 0 1-.5-.5"/>
                        <path d="M9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.5zm0 1v2A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1z"/>
                    </svg>
                    <small>Archivo</small>
                </div>
            `
        } else {
            adjuntoMensaje = ''
        }
        mensajeCitado = `
            <div class="${bgColorMentioned} rounded p-2 my-1">
                <a href="#${data.mencion.id}" data-mentioned="${data.mencion}" class="referencia-citada d-flex flex-column ${textColor} text-decoration-none" style="font-size: 15px;">
                    <small class="fw-medium ">${cabeceraMensaje}</small>
                    <small>${contenidoMensaje}</small>
                    ${adjuntoMensaje}                    
                </a>
            </div>
        `
    } else {
        mensajeCitado = ''
    }

    let adjunto = null
    if (data.url_adjunto.includes('.')) {
        const formatosImagenes = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tiff', 'tif']
        const formatosAudio = ['mp3', 'ogg', 'acc', 'wav', 'oga']
        const extension = data.url_adjunto.substring(data.url_adjunto.lastIndexOf('.') + 1);
        if (formatosImagenes.includes(extension)) {
            adjunto = `
                <a href="${data.url_adjunto}" target="_blank">    
                    <img src="${data.url_adjunto}" alt="" class="mt-1" style="max-width: 330px; max-height: 330px;" onerror="manejarArchivoEliminadoDer(this)">
                </a>
            `
        } else if (formatosAudio.includes(extension)) {
            adjunto = `
                <audio controls class="mt-1">
                    <source src="${data.url_adjunto}" type>
                        El navegador no soporta el tipo de formato del audio
                </audio>
            `
        } else {
            const nombre_archivo = data.url_adjunto.substring(data.url_adjunto.lastIndexOf('/') + 1);
            const peso = await obtenerPesoArchivo(data.url_adjunto)
            adjunto = `
                <a href="${data.url_adjunto}" class="d-flex justify-content-center align-items-center ${textColor} text-decoration-none rounded-3 my-1 p-2 gap-1" style="background-color: ${bgSecondaryColor};" target="_blank">
                    <svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" fill="currentColor" class="bi bi-file-earmark-arrow-down-fill" viewBox="0 0 16 16">
                        <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1m-1 4v3.793l1.146-1.147a.5.5 0 0 1 .708.708l-2 2a.5.5 0 0 1-.708 0l-2-2a.5.5 0 0 1 .708-.708L7.5 11.293V7.5a.5.5 0 0 1 1 0"/>
                    </svg>
                    <div>
                        <p class="mb-0">${nombre_archivo}</p>
                        <small>Tamaño: ${peso.toFixed(2)} KB</small>
                    </div>
                </a>
            `
        }
    } else {
        adjunto = ''
    }

    const dropdown = `
        <div class="dropdown dropdown-start position-absolute top-0" style="right: 5px">
            <button class="btn py-0 px-2 dropdown-toggle text-white" type="button" data-bs-toggle="dropdown" aria-expanded="false" style="border: none !important; outline: none;"></button>
            <ul class="dropdown-menu dropdown-menu-end" style="">
                <li><h6 class="dropdown-header">Opciones:</h6></li>
                <li>
                    <a href="#" class="dropdown-item responder-mensaje">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-reply" viewBox="0 0 16 16">
                            <path d="M6.598 5.013a.144.144 0 0 1 .202.134V6.3a.5.5 0 0 0 .5.5c.667 0 2.013.005 3.3.822.984.624 1.99 1.76 2.595 3.876-1.02-.983-2.185-1.516-3.205-1.799a8.7 8.7 0 0 0-1.921-.306 7 7 0 0 0-.798.008h-.013l-.005.001h-.001L7.3 9.9l-.05-.498a.5.5 0 0 0-.45.498v1.153c0 .108-.11.176-.202.134L2.614 8.254l-.042-.028a.147.147 0 0 1 0-.252l.042-.028zM7.8 10.386q.103 0 .223.006c.434.02 1.034.086 1.7.271 1.326.368 2.896 1.202 3.94 3.08a.5.5 0 0 0 .933-.305c-.464-3.71-1.886-5.662-3.46-6.66-1.245-.79-2.527-.942-3.336-.971v-.66a1.144 1.144 0 0 0-1.767-.96l-3.994 2.94a1.147 1.147 0 0 0 0 1.946l3.994 2.94a1.144 1.144 0 0 0 1.767-.96z"></path>
                        </svg>
                        Responder
                    </a>
                </li>
            </ul>
        </div>
    `
    
    const mensajeConEspacios = data.mensaje.replaceAll('\n', '<br>')
    const html = `
        <div style="max-width: 60%;" class="${alignMessage} d-flex flex-column">
            <div class="d-flex ${alignThumbnail} gap-1 ">
            <img src="/static/img/logo.png" alt="ameport_logo" width="24" height="24" class="mt-1 rounded-circle">
                <div id="${data.id_integracion}" class="${bgColor} caja-mensaje-chat position-relative" data-side=${side}>
                    <div class="mensaje-cabecera">
                        <small class="${textColor}">${formattedDate} -</small>
                        <small class="${textColor}">${data.usuario}</small>
                    </div>
                    ${mensajeCitado}
                    <div class="mensaje-adjunto">${adjunto}</div>
                    <small class="mensaje-contenido">${mensajeConEspacios}</small>
                    ${dropdown}
                </div>
            </div>
        </div>
    `
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

function chequearMensajeExistente(contacto_id, mencion_id) {
    fetch(`buscar-mensaje-mencionado/${contacto_id}/${mencion_id}/`)
    .then(response => response.json())
    .then(data => data.encontrado)
    .catch(error => console.error('Error al cargar más mensajes:', error))
}