__author__ = 'quybvs'
import argparse



from config.logging_cfg import *
from crawler.crawler import Crawler
from burner.burner import Burner

parser = argparse.ArgumentParser()
parser.add_argument('url', help="url want to download", type=str)

args = parser.parse_args()

if args.url:
    crawler = Crawler(args.url)
    crawler_rs = crawler.crawling()
    log.info("Crawler successfully")
    burner = Burner(crawler.book)
    burner_rs = burner.burning()
    log.info("Burner successfully")
    print burner_rs
else:
    log.warning("No address to download")
# burner = Burner()


