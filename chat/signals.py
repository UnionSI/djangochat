from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from usuario.models import Usuario
from .models import Integracion, Sector, SectorTarea, ContactoIntegracion, ContactoTarea, Contacto, Mensaje, MensajeAdjunto
from django.utils import timezone
from django.core.files.base import ContentFile
import base64, uuid


@receiver(post_migrate)
def crear_datos_de_prueba(sender, **kwargs):
    if sender.name == 'chat':
        usuario_admin = Usuario.objects.get(username='admin')

        archivo = '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'
        archivo_base64 = base64.b64decode(archivo)
        archivo_temporal = ContentFile(archivo_base64, name='archivo-de-prueba.jpg')

        if not Integracion.objects.filter(nombre='Test').exists() and not Integracion.objects.filter(nombre='WhatsApp').exists():
            print('Creando datos de prueba...')
            integracion_test = Integracion.objects.create(nombre='Test', activo=True)
            integracion_whatsapp = Integracion.objects.create(nombre='WhatsApp', activo=True)

            sector_chatbot = Sector.objects.create(nombre='Chatbot')
            sector_cac = Sector.objects.create(nombre='CAC')
            sector_ayudas = Sector.objects.create(nombre='Ayudas económicas')

            sectortarea_contactoinicial = SectorTarea.objects.create(nombre='Contacto inicial', sector=sector_chatbot)
            sectortarea_finalizado = SectorTarea.objects.create(nombre='Finalizado', sector=sector_chatbot)
            sectortarea_consultainicial = SectorTarea.objects.create(nombre='Consulta inicial', sector=sector_cac)
            sectortarea_aderivar = SectorTarea.objects.create(nombre='A derivar', sector=sector_cac)
            sectortarea_aderivarcupon = SectorTarea.objects.create(nombre='A derivar cupón', sector=sector_cac)
            sectortarea_aderivardevolucion = SectorTarea.objects.create(nombre='A derivar devolución/recibo', sector=sector_cac)
            sectortarea_esperandodocumentacion = SectorTarea.objects.create(nombre='Esperando documentación', sector=sector_ayudas)

            contacto_carlos = Contacto.objects.create(nombre='Carlos', apellido='García', dni='20300400', telefono='5491133334444', email='carlos@mail.com', empresa='Motorola', nro_socio='3344')
            contacto_maria = Contacto.objects.create(nombre='María', apellido='Gómez', dni='21400500', telefono='5491144445555', email='maria@mail.com', empresa='Samsung', nro_socio='4455')
            contacto_juan = Contacto.objects.create(nombre='Juan', apellido='Álvarez', dni='22500600', telefono='5491155556666', email='juan@mail.com', empresa='Philips', nro_socio='5566')
            contacto_ana = Contacto.objects.create(nombre='Ana', apellido='Fernández', dni='23600700', telefono='5491166667777', email='ana@mail.com', empresa='LG', nro_socio='6677')
            
            cont_int_carlos = ContactoIntegracion.objects.create(contacto=contacto_carlos, integracion=integracion_test)
            cont_int_maria = ContactoIntegracion.objects.create(contacto=contacto_maria, integracion=integracion_test)
            cont_int_juan = ContactoIntegracion.objects.create(contacto=contacto_juan, integracion=integracion_test)
            cont_int_ana = ContactoIntegracion.objects.create(contacto=contacto_ana, integracion=integracion_test)

            ContactoTarea.objects.create(contacto_integracion=cont_int_carlos, sector_tarea=sectortarea_consultainicial)
            ContactoTarea.objects.create(contacto_integracion=cont_int_maria, sector_tarea=sectortarea_consultainicial)
            ContactoTarea.objects.create(contacto_integracion=cont_int_juan, sector_tarea=sectortarea_aderivar)
            ContactoTarea.objects.create(contacto_integracion=cont_int_ana, sector_tarea=sectortarea_aderivarcupon)

            Mensaje.objects.create(contacto_integracion=cont_int_carlos, usuario=usuario_admin, contenido='Mensaje de prueba inicial', id_integracion=str(uuid.uuid4()))
            Mensaje.objects.create(contacto_integracion=cont_int_maria, usuario=usuario_admin, contenido='Mensaje de prueba inicial', id_integracion=str(uuid.uuid4()))
            Mensaje.objects.create(contacto_integracion=cont_int_juan, usuario=usuario_admin, contenido='Mensaje de prueba inicial', id_integracion=str(uuid.uuid4()))
            Mensaje.objects.create(contacto_integracion=cont_int_ana, usuario=usuario_admin, contenido='Mensaje de prueba inicial', id_integracion=str(uuid.uuid4()))            
            
            msj_carlos_2 = Mensaje.objects.create(contacto_integracion=cont_int_carlos, contenido='¡Hola, buen día!', id_integracion=str(uuid.uuid4()))
            msj_carlos_3 = Mensaje.objects.create(contacto_integracion=cont_int_carlos, usuario=usuario_admin, contenido='¡Buen día! ¿En qué lo puedo ayudar?', id_integracion=str(uuid.uuid4()), mensaje_citado=msj_carlos_2)
            msj_carlos_4 = Mensaje.objects.create(contacto_integracion=cont_int_carlos, contenido='¿Me podría compartir el logo de Google?', id_integracion=str(uuid.uuid4()), mensaje_citado=msj_carlos_3)
            msj_carlos_5 = Mensaje.objects.create(contacto_integracion=cont_int_carlos, usuario=usuario_admin, contenido='Sí, claro. Aquí está 👆', id_integracion=str(uuid.uuid4()))
            
            MensajeAdjunto.objects.create(archivo=archivo_temporal, formato='image', mensaje=msj_carlos_5)
            print('Datos de prueba creados...')
