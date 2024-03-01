from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from usuario.decorators import administrador_requirido
from django.http import JsonResponse
from django.contrib import messages
from bot.chatbot import responde_chatbot
from config.settings import BASE_DIR
from datetime import datetime
import os

@login_required
def bot_menu(request):
    return render(request, 'bot/bot_menu.html')

@administrador_requirido
def bot_reglas(request):
    directorio = os.path.join(BASE_DIR, 'bot', 'bot_reglas')
    context = {}
    
    archivos_rive = []
    for archivo in os.listdir(directorio):
        if archivo.endswith('.rive'):
            archivos_rive.append(archivo)
    
    if request.method == 'POST':
        archivo_elegido = request.POST.get('archivo_elegido')
        nuevo_contenido = request.POST.get('nuevo_contenido')
        
        if archivo_elegido in archivos_rive:
            try:
                ruta_archivo_antiguo = os.path.join(directorio, archivo_elegido)
                fecha_hora_actual = datetime.now().strftime("%Y%m%d%H%M%S")
                nombre_archivo_historico = f"{archivo_elegido}_{fecha_hora_actual}.rive"
                directorio_historico = os.path.join(directorio, 'historico')

                if not os.path.exists(directorio_historico):
                    os.makedirs(directorio_historico)

                ruta_archivo_historico = os.path.join(directorio_historico, nombre_archivo_historico)
                os.rename(ruta_archivo_antiguo, ruta_archivo_historico)
                
                with open(ruta_archivo_antiguo, 'w', newline='') as archivo:
                    archivo.write(nuevo_contenido)

                messages.success(request, '¡El archivo se grabó correctamente!', extra_tags='success')

            except Exception as e:
                messages.error(request, f'Error al grabar el archivo: {e}', extra_tags='danger')

        return redirect('bot:reglas')    
    else:
        if archivos_rive:
            archivo_elegido = request.GET.get('regla_bot')
            if archivo_elegido:
                ruta_archivo = os.path.join(directorio, archivo_elegido)
                with open(ruta_archivo, 'r') as archivo:
                    context['archivo'] = archivo_elegido
                    context['contenido'] = archivo.read()
            context['archivos_rive'] = archivos_rive
        return render(request, 'bot/bot_reglas.html', context)


@login_required
def bot_test(request):
    return render(request, 'bot/bot_test.html')


def bot_responde(request):
    mensaje = request.GET.get('mensaje')
    respuesta = responde_chatbot(False, None, mensaje, None)
    return JsonResponse({'status': 'success', 'data': [respuesta]})
