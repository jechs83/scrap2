import time
import schedule
from skpy import Skype

# Configuración de Skype
SKYPE_USERNAME = "+51930260230"  # Reemplaza con tu número de teléfono
SKYPE_PASSWORD = "Jazmine.2013"
CONTACTO_ID = "live:.cid.812fbc469935c7f4"  # Reemplaza con el ID del contacto

# Iniciar sesión
skype = Skype(SKYPE_USERNAME, SKYPE_PASSWORD)

# Función para enviar el mensaje
def enviar_mensaje(mensaje):
    try:
        chat = skype.contacts[CONTACTO_ID].chat  # Obtener el chat del contacto
        chat.sendMsg(mensaje)
        print(f"Mensaje enviado a {CONTACTO_ID}: {mensaje}")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")

# # Programar el envío cada 10 segundos
# schedule.every(10).seconds.do(enviar_mensaje)

# # Iniciar el bucle de ejecución
# print("Bot iniciado... Enviando mensajes cada 10 segundos.")

# while True:
#     schedule.run_pending()
#     time.sleep(1)

