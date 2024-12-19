
import logging
import pymongo
from oechsle.settings import COLLECTION_NAME
from datetime import date, datetime, timedelta

def load_datetime():
    
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
        
    return date_now, time_now, today
current_date = load_datetime()[0]

class MongoPipeline(object):


    collection_name = COLLECTION_NAME

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()



    # def process_item(self, item, spider):
    #     collection = self.db[self.collection_name]
    #     filter = { "_id":item["_id"], "sku": item["sku"]}
    #     update = {'$set': dict(item)}
    #     result = collection.update_one(filter, update, upsert=True)
    #     spider.logger.debug('Item updated in MongoDB: %s', result)
    #     return item

    def process_item(self, item, spider):
        collection = self.db[self.collection_name]
        
        # Buscar el documento existente
        existing_doc = collection.find_one({"sku": item["sku"]})
        
        if existing_doc:
            # Verificar si hay cambios en los precios
            price_changed = any([
                existing_doc.get("best_price") != item["best_price"],
                existing_doc.get("list_price") != item["list_price"],
                existing_doc.get("card_price") != item["card_price"]
            ])
            
            if price_changed:
                # Si hay cambios en precios, actualizar todo el documento
                update = {
                    '$set': dict(item)
                }
                result = collection.update_one(
                    {"sku": item["sku"]}, 
                    update
                )
                spider.logger.debug('Item updated with price changes in MongoDB: %s', result)
           
        else:
            # Si es un documento nuevo, insertarlo
            result = collection.insert_one(dict(item))
            spider.logger.debug('New item inserted in MongoDB: %s', result)
        
        return item