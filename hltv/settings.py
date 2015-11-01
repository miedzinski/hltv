import logging

BOT_NAME = 'hltv'

SPIDER_MODULES = ['hltv.spiders']
NEWSPIDER_MODULE = 'hltv.spiders'

USER_AGENT = 'hltv (http://morph.io/miedzinski/hltv)'

COOKIES_ENABLED=False

ITEM_PIPELINES = {
    'hltv.pipelines.MorphIOPipeline': 300,
}

HTTPCACHE_ENABLED=True
HTTPCACHE_EXPIRATION_SECS=0
HTTPCACHE_DIR='httpcache'
HTTPCACHE_IGNORE_HTTP_CODES=[]
HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
HTTPCACHE_POLICY='scrapy.extensions.httpcache.RFC2616Policy'

LOG_ENABLED = True
LOG_LEVEL = logging.ERROR
