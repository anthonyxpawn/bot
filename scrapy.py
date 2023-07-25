import requests
from bs4 import BeautifulSoup
import time
import asyncio
from telegram import Bot

# Configurar tu token de Telegram
TELEGRAM_TOKEN = '6582465799:AAGhEyQR3yg5OYSvIWZEgNxfbGdyHFvyZSY'

bot = Bot(TELEGRAM_TOKEN)

async def enviar_mensaje_telegram(chat_id, mensaje):
    await bot.send_message(chat_id, mensaje, parse_mode="Markdown")

async def obtener_cursos_disponibles():
    url = 'https://map.gob.do/Concursa/'

    # Agregar una cabecera de User-Agent para simular un navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Realizar la solicitud a la página utilizando la librería requests
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa (código de estado 200 indica éxito)
    if response.status_code == 200:
        # Parsear el contenido HTML utilizando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Obtener el contenido de los elementos con los ids especificados
        texto_administrativa = soup.find('p', id='textoCantidadCarreraAdministrativa').text.strip()
        texto_sanitaria = soup.find('p', id='textoCantidadCarreraSanitaria').text.strip()

        # Extraer el número de cada elemento
        numero_administrativa = int(texto_administrativa.split()[0])
        numero_sanitaria = int(texto_sanitaria.split()[0])

        # Verificar si hay nuevos cursos disponibles y enviar el mensaje
        if numero_administrativa > 0 or numero_sanitaria > 0:
            mensaje = f"¡Hay nuevos cursos disponibles! [Ve al sitio web del ministerio]({url})"
        else:
            mensaje = "No hay cursos disponibles en este momento."

        # Obtener la lista de chats donde está presente el bot
        updates = await bot.getUpdates()
        chat_ids = {update.message.chat.id for update in updates if update.message}

        # Enviar el mensaje a cada chat donde está presente el bot
        for chat_id in chat_ids:
            await enviar_mensaje_telegram(chat_id, mensaje)
    else:
        print(f"Fallo al obtener la página. Código de estado: {response.status_code}")

# Ejecutar el programa constantemente con pausas de 1 hora (3600 segundos)
async def main():
    while True:
        await obtener_cursos_disponibles()
        await asyncio.sleep(3600)  # Pausa de 1 hora entre cada ejecución

if __name__ == "__main__":
    asyncio.run(main())
