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
    if crawler_rs:
        log.info("Crawler successfully")
        burner = Burner(crawler.book)
        burner_rs = burner.burning()
        if burner_rs:
            log.info("Burner successfully")
            print burner_rs
        else:
            log.error("Can't burning")
    else:
        log.error("Can't crawling")
else:
    log.warning("No address to download")



