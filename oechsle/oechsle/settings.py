# Scrapy settings for demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from decouple import config
import logging


logging.getLogger('pymongo').setLevel(logging.WARNING)

BOT_NAME = "oechsle"
URLLENGTH_LIMIT = 10000  # Ajusta el límite según tus necesidades

SPIDER_MODULES = ["oechsle.spiders"]
NEWSPIDER_MODULE = "oechsle.spiders"

ITEM_PIPELINES = {
    'oechsle.pipelines.MongoPipeline': 300,
}

MONGO_URI = config("MONGODB")

MONGO_DATABASE = config("db_oechsle")
COLLECTION_NAME = "scrap4"

DEBUG_LEVEL = "INFO"
##### PARA PRUEBAS LOCASL SIN AFECTAR LA BASE DE DATOS ORIGINAL

# MONGO_DATABASE = config("db_oechsle")
# COLLECTION_NAME = "scrap2"

RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408, 429]

# Set the maximum number of retries for each request
RETRY_TIMES = 3  # Adjust this value as neededRETRY_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408, 429]

# Set the maximum number of retries for each request

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "demo (+http://www.yourdomain.com)"

# Obey robots.txt rules
#ROBOTSTXT_OBEY = True
#USER_AGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32
# LOG_ENABLED = True
# LOG_LEVEL = 'DEBUG'
# LOG_FILE = 'scrapy.log'
#DOWNLOAD_DELAY = 0.1  # 100 ms de retraso
CONCURRENT_REQUESTS = 32 # Incrementa el número de solicitudes simultáneas 
ROBOTSTXT_OBEY=False # Desactiva el cumplimiento de robots.txt 

    





# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "demo.middlewares.DemoSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "demo.middlewares.DemoDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "demo.pipelines.DemoPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

