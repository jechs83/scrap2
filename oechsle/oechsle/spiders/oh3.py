import scrapy
from pymongo import MongoClient
from datetime import datetime
import subprocess

from time import time
from decouple import config
# from mensaje import *

# enviar_mensaje_telegram("Sacando Oe y Vea...         ")

class ProductSpider(scrapy.Spider):
    name = "oechsleee"
    allowed_domains = ["oechsle.pe"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = MongoClient(config("MONGODB"), serverSelectionTimeoutMS=5000)
        self.db = self.client['all']  #bd
        self.collection_urls = self.db['bdoe']  #URLs
        self.collection_products = self.db['productos']  #productos
    custom_settings = {
            'HTTPCACHE_ENABLED': False,  # Desactiva la caché en Scrapy.
            'COOKIES_ENABLED': False
            }
    step = 50 

    def start_requests(self):
        #self.collection_products.delete_many({})
        urls = self.collection_urls.find({}, {"enlaces": 1, "_id": 0})
        
        for url_entry in urls:
            base_url = url_entry.get("enlaces")
            if base_url:
                start = 0
                yield self.make_request(base_url, start)

    def make_request(self, url, start):
        _from = start
        _to = _from + self.step - 1
        timestamp = int(time())
        full_url = f"{url}_from={_from}&_to={_to}&fq=specificationFilter_4664:Oechsle&fq=specificationFilter_4664:Promart&fq=specificationFilter_4664:plazaVea&timestamp={timestamp}"
        
        headers = {
        'Cache-Control': 'no-cache',  # Evitar caché del servidor
        'Pragma': 'no-cache'}          # Otra directiva para evitar la caché

        return scrapy.Request(full_url, callback=self.parse, meta={'base_url': url, 'start': start}, headers=headers)

    def parse(self, response):
        base_url = response.meta['base_url']
        start = response.meta['start']

        data = response.json()

        if not data:
            self.logger.info(f"No data found for URL: {response.url}")
            return

        for product in data:
            product_id = product.get("productId", "N/A")
            product_name = product.get("productName", "N/A").upper()
            brand = product.get("brand", "N/A")
            link = product.get("link", "N/A")

            #long_url = link
            #api_token = '8ef0b5320f84b361f12bf40030418fb9608857ad'
            #link = shorten_url(long_url, api_token)
            #imagen = "https://ripleype.imgix.net/https%3A%2F%2Fmedia-prod-use-1.mirakl.net%2FSOURCE%2Fe5972167b9d14307b7cafa44ab7105cd?w=750&h=555&ch=Width&auto=format&cs=strip&bg=FFFFFF&q=60&trimcolor=FFFFFF&trim=color&fit=fillmax&ixlib=js-1.1.0&s=9c5479a7d8f7e3ff6321285d19132fc1"

            #cats = product.get("categories", [])
            #categoria = product.get("categoriesIds", [])

            for sub_item in product.get("items", []):
                images = sub_item.get("images", [])
                imagen = images[0].get("imageUrl") if images else "https://ripleype.imgix.net/https%3A%2F%2Fmedia-prod-use-1.mirakl.net%2FSOURCE%2Fe5972167b9d14307b7cafa44ab7105cd?w=750&h=555&ch=Width&auto=format&cs=strip&bg=FFFFFF&q=60&trimcolor=FFFFFF&trim=color&fit=fillmax&ixlib=js-1.1.0&s=9c5479a7d8f7e3ff6321285d19132fc1"
                #imagen = sub_item.get("images", [{}])[0].get("imageUrl")
                sellers = sub_item.get("sellers", [])

                for seller in sellers:
                    seller_id = seller.get("sellerName", "N/A")
                    seller_id = seller_id.lower().replace(" ", "").upper()
                    product_id = product_id + seller_id + "OE"
                    carro = seller.get("addToCartLink", "N/A")
                    commertial_offer = seller.get("commertialOffer", {})
                    current_price = commertial_offer.get("Price", 0.0)
                    current_list_price = commertial_offer.get("ListPrice", 0.0)

                    if current_price > 0.0 and current_list_price > 0.0:
                        oh_dsct = 0.0
                        promotion_teasers = commertial_offer.get("PromotionTeasers", [])
                        for teaser in promotion_teasers:
                            parameters = teaser.get("Effects", {}).get("Parameters", [])
                            if len(parameters) > 1:
                                oh_dsct = parameters[1].get("Value")

                        #oh_price = round(current_list_price - float(oh_dsct), 2) if oh_dsct else 0.0
                        #descuento2 = round((100 - ((oh_price / current_list_price) * 100)), 0) if oh_price else 0.0
                        #descuento = round((100 - ((current_price / current_list_price) * 100)), 0) if current_list_price > 0 else 0.0
                        #else:
                        if oh_dsct == 0:
                            oh_price = 0.0
                        else:
                            if(float(current_list_price)-float(oh_dsct))>float(current_price):
                                oh_price = round(float(current_price)-float(oh_dsct),2)
                            else:
                                oh_price = round(float(current_list_price)-float(oh_dsct),2)

                        descuento2 = round((100 - ((oh_price / current_list_price) * 100)), 0) if oh_price else 0.0
                        descuento1 = round((100 - ((current_price / current_list_price) * 100)), 0) if current_list_price > 0 else 0.0
                        descuento = round(float(max(descuento1, descuento2)), 0)

                        hora_extraccion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

                        valores = [x for x in (current_list_price, current_price, oh_price) if x != 0]
                        minimo = min(valores) if valores else "abc"  # Devuelve None si todos son 0

                        producto = {
                            #"oh_dsct":oh_dsct,
                            "_id": product_id,
                            "Producto": product_name,
                            "Vendedor": seller_id,
                            "brand": brand,
                            "link": link,
                            "imageUrl": imagen,
                            "hora_extraccion": hora_extraccion,
                            "Precio": current_price,
                            "Preciodelista": current_list_price,
                            "DescuentoEspecifico": oh_price,
                            "minimo":minimo,
                            "carro":carro,
                            "Descuento": descuento,
                            #"Descuento2": descuento2
                            #"categoria": categoria,
                            #"cats": cats
                        }

                        #self.collection_products.insert_one(producto)
                        self.collection_products.update_one(
                        {"_id": product_id},  # Filtro para encontrar el documento
                        {"$set": producto},         # Datos a actualizar
                        upsert=True)                 # Insertar si no se encuentra el documento

        start += self.step
        yield self.make_request(base_url, start)
    
    # def closed(self, reason):
    #     try:
    #         # Ejecuta el archivo .bat en una nueva terminal
    #         subprocess.Popen(['start', 'cmd', '/c', 'vea1.bat'], shell=True)
    #     except Exception as e:
    #         self.logger.error("Error al ejecutar el archivo .bat: %s", e)
