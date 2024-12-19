import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pymongo
from decouple import config

import unicodedata

# Assuming links() and lista_block() are defined elsewhere or can be replaced with static data
# For demonstration, I'll use placeholder functions
def links():
    # Replace with your actual logic to fetch URLs
    return [
        ["https://www.oechsle.pe/api/catalog_system/pub/products/search/?&O=OrderByPriceDESC&_from={}&_to={}&fq=C:/161/&"]
    ]

def lista_block(db):
    # Replace with your actual logic to fetch blocked brands
    return ["N/A"]

class OechsleScraper:
    def __init__(self, u):
        self.u = int(u)
        self.client = pymongo.MongoClient(config("MONGODB"), serverSelectionTimeoutMS=5000)
        self.urls = links()[self.u - 1]
        self.db = self.client['oechsle']
        self.collection_name = self.db['scrap6']
        self.block_list = lista_block(self.db)
        self.seen_skus = set()
        self.duplicate_count = 0
        self.batch_data = []
        self.collected_skus = []
        self.image = "https://ripleype.imgix.net/https%3A%2F%2Fmedia-prod-use-1.mirakl.net%2FSOURCE%2Fe5972167b9d14307b7cafa44ab7105cd?w=750&h=555&ch=Width&auto=format&cs=strip&bg=FFFFFF&q=60&trimcolor=FFFFFF&trim=color&fit=fillmax&ixlib=js-1.1.0&s=9c5479a7d8f7e3ff6321285d19132fc1"

    def start_requests(self):
        # for i, v in enumerate(self.urls):
        #     url_base = f"{v[0]}"
        #     print(f"URL base: {url_base}")
            url_base ="https://www.oechsle.pe/api/catalog_system/pub/products/search/?&O=OrderByPriceDESC&_from={}&_to={}&fq=C:/161/&"

            items_per_page = 25
            total_iterations = 100

            for iteration in range(total_iterations):
                from_value = iteration * items_per_page
                to_value = from_value + (items_per_page - 1)
                url = url_base.format(from_value, to_value)
                url = url + "fq=specificationFilter_4664:Oechsle&fq=specificationFilter_4664:Promart&fq=specificationFilter_4664:plazaVea"
                print(url)
                self.parse_products(url)

    def parse_products(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            return
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from URL {url}: {e}")
            return

        if not data:
            print(f"No data found for URL: {url}")
            return

        for product in data:
            item = {}
            item["brand"] = str(product.get("brand", "N/A")).lower()
            item["brand"] = unicodedata.normalize('NFD', item["brand"])
            item["brand"] = ''.join(char for char in item["brand"] if unicodedata.category(char) != 'Mn')

            if item["brand"] in self.block_list:
                continue

            item["sku"] = product.get("items", [])[0].get("itemId","N/A")
            item["product"] = product.get("productName", "N/A")
            item["link"] = product.get("link", "N/A")
            item["image"] = product.get("items", [])[0].get("images", [])[0].get("imageUrl", self.image)
            item["market"] = product.get("items", [])[0].get("sellers", [])[0].get("sellerName", "N/A")
            item["best_price"] = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", {}).get("Price", 0.0)
            item["list_price"] = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", {}).get("ListPrice", 0.0)
            test = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", {}).get("FullSellingPrice", 0.0)
            try:
                dsct = product.get("items", [])[0].get("sellers", [])[0].get("commertialOffer", {}).get("PromotionTeasers")[0].get("Effects").get("Parameters")[1].get("Value")
            except:
                dsct = 0

            if dsct != 0:
                item["card_price"] = round(float(item["best_price"]) - float(dsct))
            else:
                item["card_price"] = 0

            if item["card_price"] and item["list_price"] and item["best_price"] > 0:
                item["card_dsct"] = round((100 - ((item["card_price"] * 100 / item["list_price"]))), 0) if item["list_price"] > 0 else 0.0
            else:
                item["card_dsct"] = round((100 - ((item["best_price"] * 100 / item["list_price"]))), 0) if item["list_price"] > 0 else 0.0

            item["web_dsct"] = round((100 - ((item["best_price"] * 100 / item["list_price"]))), 0) if item["list_price"] > 0 else 0.0

            if item["card_price"] == 0:
                item["web_dsct"] = item["card_dsct"]
                item["card_dsct"] = 0

            current_datetime = datetime.now()
            item["date"] = current_datetime.strftime("%d/%m/%Y")
            item["time"] = current_datetime.strftime("%H:%M:%S")

            print(item["brand"])
            print(item["market"])
            print("best_price " + str(item["best_price"]))
            print("list_price " + str(item["list_price"]))
            print("card_price " + str(item["card_price"]))
            print(str(item["card_dsct"]) + "%")
            print("test_price " + str(test))
            print(dsct)
            print(item["link"])
            print()

            self.save_item(item)

    def save_item(self, item):
        collection = self.db["scrap"]
        filter = {"sku": item["sku"]}
        update = {'$set': dict(item)}
        result = collection.update_one(filter, update, upsert=True)

    def close(self):
        stats = {}  # Placeholder for stats
        current_time = datetime.now()
        end_time = current_time
        start_time = current_time  # Placeholder for start time
        duration = (current_time - start_time).total_seconds()

        print()
        print(start_time)
        print(current_time)
        print(duration)

        db_variable = self.client["oechsle"]
        end_time_doc = {
            "_id": int(self.u),
            "spider_name": "oh2",
            "start_time": str(start_time),
            "end_time": end_time,
            "duration_seconds": round(duration),
            "items_scraped": stats.get('item_scraped_count', 0),
            "status": "completed",
            "lista": int(self.u)
        }

        update_doc = {
            "$set": end_time_doc
        }

        try:
            db_tai = db_variable["task_time"]
            result = db_tai.update_one(
                {"_id": int(self.u)},
                update_doc,
                upsert=True
            )
            print(f"Documento insertado")
        except Exception as e:
            print(f"Error al insertar en MongoDB: {e}")
        finally:
            self.client.close()

if __name__ == '__main__':
    # Example usage:
    scraper = OechsleScraper(u=1)  # Replace 1 with the desired 'u' value
    scraper.start_requests()
    scraper.close()