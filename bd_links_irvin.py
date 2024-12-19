import csv
from pymongo import MongoClient
from decouple import config

# Conexión a MongoDB
client = MongoClient(config("MONGODB"), serverSelectionTimeoutMS=5000)
db = client['all']  # Nombre de la base de datos
collection = db['bdoe']  # Nombre de la colección

# Cargar datos desde el archivo CSV
csv_file = 'datos.csv'

# Leer y grabar en MongoDB
with open("/Users/javier/GIT/scrap2/enlaces.csv", 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    datos = []
    for row in reader:
        row['_id'] = (row['_id'])  # Asegurar que _id sea entero
        datos.append(row)
    
    # Insertar los datos
    if datos:
        try:
            collection.insert_many(datos, ordered=False)
            print("Datos grabados exitosamente.")
        except Exception as e:
            print(f"Error al insertar los datos: {e}")