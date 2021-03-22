from telegram.ext import Updater, CommandHandler
import datos
import logging
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    datefmt='%H:%M:%S',
    level=logging.INFO,
    filename= 'log',
    filemode='a'
    )
logger = logging.getLogger(datos.nombreBot)

url = datos.urlPolen
querystring = {"lat":"37.883333","lng":"-4.766667"}
headers = {
    'x-api-key': datos.idApi,
    'Content-type': "application/json"
    }

def start(update, context):
    logger.info('Mensaje start')
    context.bot.send_message(chat_id=update.effective_chat.id, text='Mensaje recibido')

def nivelPolen(nivel):
    #Baja: < 10 granos/metro cúbico
    #Media: 10 - 50 granos/metro cúbico
    #Alta: > 50 granos/metro cúbico
    if nivel < 10:
        return "Bajo"
    elif nivel >= 10 and nivel < 50:
         return "Medio"
    elif nivel >= 50:
        return "Alto"

def gramineas(update, context):
    requestPost = requests.request("GET", url, headers=headers, params=querystring)
    respuesta = requestPost.json()
    nivel = (respuesta["data"][0]["Count"]["grass_pollen"])
    texto ="Mensaje gramineas " +  nivelPolen(nivel) + " - " + nivel
    context.bot.send_message(chat_id = update.effective_chat.id,text = texto)
    logger.info(texto)


if __name__ == '__main__':
    updater = Updater(token=datos.idbot)
    dispatcher = updater.dispatcher

    #comandos
    dispatcher.add_handler(CommandHandler('start',start))
    dispatcher.add_handler(CommandHandler('graminea', gramineas))

    updater.start_polling()
    updater.idle()