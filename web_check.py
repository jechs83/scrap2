import requests
from skpy import Skype

# Función para verificar el estado de la web
def verificar_sitio_web(url):
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            print(f"El sitio web {url} está activo.")
            return f"🟢 El sitio web {url} está en LINEA 🟢."
        else:
            print(f"El sitio web {url} está caído. Código de estado: {respuesta.status_code}")
            return f"🔴 El sitio web {url} está en CAIDA 🔴."
    except requests.exceptions.RequestException as e:
        print(f"Error al intentar acceder a {url}: {e}")
        return f"🔴 El sitio web {url} está en CAIDA 🔴."

# Configuración de Skype
SKYPE_USERNAME = "+51930260230"  # Reemplaza con tu número de teléfono
SKYPE_PASSWORD = "Jazmine.2013"
GRUPO_ID = "19:f85673cba18b4672b5c5f9e5586fd865@thread.skype"  # ID del grupo de Skype

# Iniciar sesión
try:
    skype = Skype(SKYPE_USERNAME, SKYPE_PASSWORD)
    print("Sesión iniciada correctamente.")
except Exception as e:
    print(f"Error al iniciar sesión: {e}")
    exit()

# Función para enviar mensaje
def enviar_mensaje(mensaje):
    try:
        chat = skype.chats[GRUPO_ID]  # Obtener el grupo
        if chat:
            chat.sendMsg(mensaje)
            print(f"Mensaje enviado al grupo: {mensaje}")
        else:
            print(f"El grupo con ID {GRUPO_ID} no fue encontrado.")
    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")

# Verificar el estado de la web y enviar mensaje
url = "https://sparxworks.com/"
mensaje = verificar_sitio_web(url)
enviar_mensaje(mensaje)