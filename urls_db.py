

import pymongo
from decouple import config


# Establecer la conexión a MongoDB
cliente = pymongo.MongoClient(config("MONGODB"))
base_de_datos = cliente["oechsle"]
coleccion = base_de_datos["links"]

lista1=[];lista2=[];lista3=[];lista4=[];lista5=[];lista6=[];lista7=[];lista8=[];lista9=[];lista10=[];lista11=[];lista12=[];lista13=[];lista14=[];lista15=[];lista16=[];lista17=[];lista18=[];lista19=[]; lista20 =[]


# Obtener los documentos de la colección

# Iterar sobre los documentos y clasificar según el valor de "lista"
def links():
    documentos = coleccion.find()
    for documento in documentos:
        lista = documento["lista"]
        url = documento["url"]
        page = documento["page"]
        try:
            json_link = documento["json_link"]
        except:  
            json_link = None

    
        for i in range(1, 20):  # Start the loop from 1 instead of 0
            if lista == i:
                # Agregar a la lista correspondiente en el formato requerido
                if i == 1:
                    lista1.append((url, json_link, page))
                elif i == 2:
                    lista2.append((url, json_link, page))
                elif i ==3:
                    lista3.append((url, json_link, page))
                elif i == 4:
                    lista4.append((url, json_link, page))
                elif i == 5:
                    lista5.append((url, json_link, page))
                        
                elif i == 6:
                    lista6.append((url, json_link, page))
                elif i == 7:
                    lista7.append((url, json_link, page))
                elif i == 8:
                    lista8.append((url, json_link, page))
                elif i == 9:
                    lista9.append((url, json_link, page))
                elif i == 10:
                    lista10.append((url, json_link, page))
                elif i == 11:
                    lista11.append((url, json_link, page))
                elif i == 12:
                    lista12.append((url, json_link, page))
                elif i == 13:
                    lista13.append((url, json_link, page))
                elif i == 14:
                    lista14.append((url, json_link, page))
                elif i == 15:
                    lista15.append((url, json_link, page))
                elif i == 16:
                    lista16.append((url, json_link, page))
                elif i == 17:
                    lista17.append((url, json_link, page))
                elif i == 18:
                    lista18.append((url, json_link, page))
                elif i == 19:
                    lista19.append((url, json_link, page))
                elif i == 20:
                    lista20.append((url, json_link, page))

    return lista1,lista2,lista3,lista4,lista5,lista6,lista7,lista8,lista9,lista10,lista11,lista12,lista13,lista14,lista15,lista16,lista17,lista18,lista19, lista20 






def lista_block( db ):
    # Conexión a la base de datos MongoDB


    db = cliente['black_list']
    return db.block_brand.distinct('brand')
