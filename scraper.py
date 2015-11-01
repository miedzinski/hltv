from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import initialize_db  # for side effect


process = CrawlerProcess(get_project_settings())
process.crawl('results')
process.start()
