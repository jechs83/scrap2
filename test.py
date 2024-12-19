from skpy import Skype

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

# Enviar mensaje de prueba
try:
    chat = skype.chats[GRUPO_ID]
    chat.sendMsg("Mensaje de prueba desde Skype Bot.")
    print("Mensaje enviado correctamente.")
except Exception as e:
    print(f"Error al enviar el mensaje: {e}")