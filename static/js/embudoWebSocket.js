const globalSocket = new WebSocket('wss://' + window.location.host + '/ws/global/');

globalSocket.onopen = function(e) {
    console.log('Global WebSocket opened');
};

globalSocket.onclose = function(e) {
    console.log('Global WebSocket closed');
};

globalSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    console.log('globalConsumer onmessage');

    switch (data.type) {
        case 'chat_message':
            handleLastMessage(data)
            break
        case 'sector_change':
            handleRoomUpdate(data);
            break;
        default:
            console.error('Unknown message type: ', data.type);
    }
};

function formatDate(date) {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const hours = date.getHours();
    const minutes = date.getMinutes();
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

function handleLastMessage(data) {
    const contacto = document.querySelector(`[data-contacto="${data.room}"]`)
    console.log('recibiendo mensaje de room', data.room, '-', data.message)
    console.log(contacto)
    if (contacto) {
        contacto.querySelector('[data-usuario]').innerText = `${data.username}: `
        contacto.querySelector('[data-mensaje]').innerText = data.message;
    }
}

function handleRoomUpdate(data) {
    // Si existe la tarjeta en este cliente, eliminarla
    const tarjetaContactoExistente = document.querySelector(`[data-contacto="${data.contacto}"]`)
    if (tarjetaContactoExistente) {
        tarjetaContactoExistente.remove()
    }
    // Si existe la tarjeta en este cliente, agregarla con la nueva información
    const sector = document.querySelector('[data-sector]').dataset.sector
    if (sector == data.sector) {
        const sectorTarea = document.querySelector(`[data-sector_tarea="${data.sector_tarea}"]`)
        if (sectorTarea) {
            const tarjetaDefault = document.querySelector('#tarjeta-default')
            const nuevaTarjetaContacto = tarjetaDefault.cloneNode(true)
            nuevaTarjetaContacto.dataset.contacto = data.contacto
            nuevaTarjetaContacto.querySelector('[data-slug]').href = data.slug;
            if (!data.no_leido) {
                nuevaTarjetaContacto.querySelector('[data-no_leido]').remove();
            }
            nuevaTarjetaContacto.querySelector('[data-thumbnail]').src = data.thumbnail;
            nuevaTarjetaContacto.querySelector('[data-cabecera]').innerText = data.cabecera;
            nuevaTarjetaContacto.querySelector('[data-dni]').innerText = data.dni;
            nuevaTarjetaContacto.querySelector('[data-usuario]').innerText = data.usuario;
            nuevaTarjetaContacto.querySelector('[data-mensaje]').innerText = data.mensaje;
            nuevaTarjetaContacto.querySelector('[data-fecha]').innerText = data.fecha;
            nuevaTarjetaContacto.classList.remove('display-none-important')
            sectorTarea.appendChild(nuevaTarjetaContacto)
            const forms = nuevaTarjetaContacto.querySelectorAll('.form-sector-change')
            forms.forEach( form => escucharCambioSector(form))
        }
    }
}

function escucharCambioSector(form) {
    form.addEventListener('submit', function(e) {
        e.preventDefault()
        const sector = form.dataset.sector_destino;
        const sectorTarea = form.dataset.tarea_sector_destino;
        const divContacto = form.closest('[data-contacto]')
        const contacto = divContacto.dataset.contacto;
        const slug = divContacto.querySelector('[data-slug]').getAttribute('href');
        let noLeido = divContacto.querySelector('[data-no_leido]');
        noLeido = noLeido !== null;
        const thumbnail = divContacto.querySelector('[data-thumbnail]').getAttribute('src');
        const cabecera = divContacto.querySelector('[data-cabecera]').innerText.trim();
        const dni = divContacto.querySelector('[data-dni]').innerText.trim();
        const usuario = divContacto.querySelector('[data-usuario]').innerText.trim();
        const mensaje = divContacto.querySelector('[data-mensaje]').innerText.trim();
        const fecha = divContacto.querySelector('[data-fecha]').innerText.trim();

        console.log({
            'type': 'sector_change',
            'sector': sector,
            'sector_tarea': sectorTarea,
            'contacto': contacto,
            'slug': slug,
            'no_leido': noLeido,
            'thumbnail': thumbnail,
            'cabecera': cabecera,
            'dni': dni,
            'usuario': usuario,
            'mensaje': mensaje,
            'fecha': fecha,
        })
    
        globalSocket.send(JSON.stringify({
            'type': 'sector_change',
            'sector': sector,
            'sector_tarea': sectorTarea,
            'contacto': contacto,
            'slug': slug,
            'no_leido': noLeido,
            'thumbnail': thumbnail,
            'cabecera': cabecera,
            'dni': dni,
            'usuario': usuario,
            'mensaje': mensaje,
            'fecha': fecha,
        }));        
    });
}

const forms = document.querySelectorAll('.form-sector-change')
forms.forEach( form => escucharCambioSector(form))