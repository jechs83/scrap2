import scrapy
from oechsle.items import OechsleItem
import datetime
from datetime import datetime
from datetime import date
import pymongo
from oechsle.spiders.urls_db import *
from decouple import config
# from oechsle.spiders.link_json import json_link
from datetime import datetime, timezone
import unicodedata

class OhSpider(scrapy.Spider):
    name = "oh"
    allowed_domains = ["oechsle.pe"]    

    def __init__(self, *args, **kwargs):
        super(OhSpider, self).__init__(*args, **kwargs)
        self.u = int(getattr(self, 'u', '0'))
        self.client = pymongo.MongoClient(config("MONGODB"), serverSelectionTimeoutMS=5000)
        self.urls = links()[self.u - 1]
        self.db = self.client['oechsle']
        self.collection_name = self.db['scrap4']
        self.block_list = lista_block(self.db )

    
        self.seen_skus = set()
        self.duplicate_count = 0
        self.batch_data = []
        self.collected_skus = []

        self.image = "https://ripleype.imgix.net/https%3A%2F%2Fmedia-prod-use-1.mirakl.net%2FSOURCE%2Fe5972167b9d14307b7cafa44ab7105cd?w=750&h=555&ch=Width&auto=format&cs=strip&bg=FFFFFF&q=60&trimcolor=FFFFFF&trim=color&fit=fillmax&ixlib=js-1.1.0&s=9c5479a7d8f7e3ff6321285d19132fc1"

        #self.lista = self.brand_allowed()[int(self.b)]  # Initialize self.lista based on self.b
    step = 50

    def start_requests(self):
       
        for i, v in enumerate(self.urls):

                # Obtener la URL base
            url_base = f"{v[0]}"
            print(f"URL base: {url_base}")

            items_per_page = 25  # Tamaño del rango para cada iteración
            total_iterations = 100  # Número total de iteraciones

            for iteration in range(total_iterations):
                # Calcular los rangos
                from_value = iteration * items_per_page
                to_value = from_value + (items_per_page - 1)

                # Formatear la URL con los valores calculados
                url = url_base.format(from_value, to_value)
                url = url +"fq=specificationFilter_4664:Oechsle&fq=specificationFilter_4664:Promart&fq=specificationFilter_4664:plazaVea"

                print(url)

           

                yield scrapy.Request(url, self.parse_products)

            # for e in range(50):
                    
             
            #         web_3 = "&fq=specificationFilter_4664:Oechsle&fq=specificationFilter_4664:Promart&fq=specificationFilter_4664:plazaVea"
            #         url = v[0]+"_from="+str(e*50)+"&_to="+str(49+e*50)+web_3
            #         #url = v[0]+str(e)+v[1]
            #         #yield scrapy.Request(url, self.parse)
            #         yield scrapy.Request(url, self.collect_skus, dont_filter=True)

                    


    # def collect_skus (self, response):
       
    #         json_data = response.text
            
    #         products = json.loads(json_data)

    
    
    #         # products = products.get('data', {}).get("results", {})
   
    #         for product in products:
    #             sku = product["productId"]

    #             self.collected_skus.append(sku)
           
    #             a = ",".join([f'productId:{pid}' for pid in self.collected_skus])
             

    #         base_url = "https://www.oechsle.pe/api/catalog_system/pub/products/search/?fq="
    #         try:
    #             final_url = f"{base_url}{a}"
    #             #print(final_url)
    #         except:
    #           return
            

    #         yield scrapy.Request(final_url, self.parse_products, dont_filter=True)


#    https://www.oechsle.pe/api/catalog_system/pub/products/search/?fq=productId:2695593,productId:2667782,productId:2406089,productId:2695594,productId:2657899,productId:2605306,productId:2583514,productId:2429647,productId:2583515,productId:2559414,productId:2453752,productId:2667787,productId:2722493,productId:2559430,productId:2722490,productId:2477892,productId:2638446,productId:2559418,productId:2559424,productId:2690621,productId:2690622,productId:2311863,productId:2613778,productId:2605301,productId:2695598,productId:2429622,productId:2657898,productId:2239992,productId:2561619,productId:2429616,productId:2583512,productId:2603842,productId:2587831,productId:2695591,productId:2540205,productId:2640907&_from=0&_to=49



    def parse_products(self, response):

        item = OechsleItem()

        data = response.json()

        if not data:
            self.logger.info(f"No data found for URL: {response.url}")
            return

        for product in data:
           # print(lista_block(self.db ))
           
            item["brand"] = str(product.get("brand", "N/A")).lower()
            item["brand"] = unicodedata.normalize('NFD', item["brand"])
            item["brand"] = ''.join(char for char in item["brand"] if unicodedata.category(char) != 'Mn')
      
            if  item["brand"]  in self.block_list:
                continue

            #item["sku"] = product.get("productId", "N/A")     
            item["sku"] = product.get("items", [])[0].get("itemId","N/A") 
            item["product"] = product.get("productName", "N/A")
            item["link"] = product.get("link", "N/A")
            item["image"] = product.get("items", [])[0].get("images", [])[0].get("imageUrl", self.image)
            item["market"] = product.get("items", [])[0].get("sellers", [])[0].get("sellerName", "N/A")
            item["best_price"] = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", []).get("Price",0.0)
            item["list_price"] = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", []).get("ListPrice",0.0)
            test = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", []).get("FullSellingPrice",0.0)
            try:
                dsct = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", []).get("PromotionTeasers")[0].get("Effects").get("Parameters")[1].get("Value")
            except:dsct = 0

            if dsct !=0 :
        
                item["card_price"] = round(float(item["best_price"]) - float(dsct))
            else:
                item["card_price"] =0


            if item["card_price"] and item["list_price"] and item["best_price"] >0:
                item["card_dsct"]  = round((100 - ((item["card_price"]*100 / item["list_price"] ))), 0) if item["list_price"] > 0 else 0.0
                #item["web_dsct"]  = round((100 - ((item["best_price"]*100 / item["list_price"] ))), 0) if item["list_price"] > 0 else 0.0


            else:
                item["card_dsct"]  = round((100 - ((item["best_price"]*100 / item["list_price"] ))), 0) if item["list_price"] > 0 else 0.0


                
            item["web_dsct"]  = round((100 - ((item["best_price"]*100 / item["list_price"] ))), 0) if item["list_price"] > 0 else 0.0

            if item["card_price"] ==0:

                item["web_dsct"] = item["card_dsct"] 
                item["card_dsct"]  = 0

            current_datetime = datetime.now()
            item["date"] = current_datetime.strftime("%d/%m/%Y")
            item["time"] = current_datetime.strftime("%H:%M:%S")
            

            producto  = {

                "sku" : item["sku"],
                "_id" : item["sku"],
                "product" : item["product"],
                "brand" : item["brand"],
                "link" : item["link"],
                "best_price" : item["best_price"],
                "list_price" : item["list_price"],
                "web_dsct" : item["web_dsct"],
                "image" : item["image"],
                'market': item["market"],
                "date" : item["date"],
                "time" : item["time"] ,
                "home_list" : "www.oechsle.pe",
                "card_price" : item["card_price"],
                "card_dsct" : item["card_dsct"],

            }

            print(producto)

            self.collection_name.update_one(
            {"sku": item["sku"]},  # Filtro para encontrar el documento
            {"$set": producto},         # Datos a actualizar
            upsert=True)                 # Insertar si no se encuentra el documento


           
            # print(item["brand"])
            # print(item["market"])
            # print("best_price "+str(item["best_price"]))
            # print("list_price "+str(item["list_price"]))
            # print("card_price "+str(item["card_price"]))
            # print( str(item["card_dsct"]) +"%")
            # print("test_price "+str(test))
            # print(dsct)
            # print(item["link"])

           

            print()
            # start += self.step
            # yield self.make_request(url, start)
    

            # yield item

                       

            # collection = self.db["scrap"]
            # filter = { "sku": item["sku"]}
            # update = {'$set': dict(item)}
            # result = collection.update_one(filter, update, upsert=True)



    def closed(self, reason):
        """Método que se ejecuta cuando el spider termina"""
        stats = self.crawler.stats.get_stats()
     
        current_time = datetime.now(timezone.utc)    
        end_time = current_time
        # Obtener tiempos
        start_time = stats.get('start_time').replace(tzinfo=timezone.utc)  
        # Calcular duración
        duration = (current_time - start_time).total_seconds()
        
        print()
        print(start_time)
        print(current_time)
        print(duration)
        
   
        
        db_variable = self.client["oechsle"]
        end_time_doc = {
            "_id": int(getattr(self, 'u', '0')),
            "spider_name": self.name,
            "start_time": str(start_time),
            "end_time": end_time,
            "duration_seconds": round(duration),
            "items_scraped": stats.get('item_scraped_count', 0),
            "status": "completed",
            "lista": int(getattr(self, 'u', '0'))
        }

        update_doc = {
                "$set": end_time_doc
            }
       
        try:
            db_tai = db_variable["task_time"]
            #result = db_tai.insert_one(end_time_doc)
            result = db_tai.update_one(
                {"_id": int(getattr(self, 'u', '0'))},  # Filtro por ID
                update_doc,
                upsert=True  # Crear documento si no existe
            )
            print(f"Documento insertado")
        except Exception as e:
            print(f"Error al insertar en MongoDB: {e}")
        finally:
            self.client.close()