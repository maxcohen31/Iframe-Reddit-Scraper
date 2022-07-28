import json
import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

class SpiderEmail(scrapy.Spider):
    name = 'email_spidy'

    allowed_domains = [
        'federbridge.it/'
    ]
    start_urls = [
        'https://www.federbridge.it/SocSp/ChkFS.asp?FS=F',
    ]

    headers = {    
        'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    }

    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'AUTOTHROTTLE_ENABLED': True,
    }

    # spider's entry point
    def start_requests(self):
        
        with open('bridge_asso.txt') as f:
            links = f.read().split('\n')
        
        # loop over list of initial links to extract data from
        for link in links:
            yield scrapy.Request(
                url=link,
                headers=self.headers,
                callback=self.parse_email
            )  

    def parse_email(self, response):
        
        data = {
            'email': response.xpath("//a/@href")[2].get().replace('mailto:', '')
        }

        # save data onto json file
        with open('email.jsonl', 'a+') as f:
            f.write(json.dumps(data) + '\n')

# main driver
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SpiderEmail)
    process.start()