import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess

class SpiderBridge(scrapy.Spider):
    name = 'bridge'

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
    
    def start_request(self):
        for url in self.start_urls:
            yield Request(
                url=email_url,
                headers=self.headers,
                callback=self.parse
            )

    def parse(self, response):

        print('***** PARSING ******')

        numbers = response.xpath("//span[@class='COLviolaChiaro']/text()").getall()
        only_numbs = [i for i in numbers if i[0] == 'F' or i[0] == 'G']
        info_url = 'https://www.federbridge.it/regioni/dettAss.asp?codice='

        complete_urls = []

        for n in only_numbs:
            complete_urls.append(f"{info_url+n}")
        
        for url in complete_urls:
            with open('bridge_asso.txt', 'a+') as f:
                f = f.write(f"{url}\n")

# main driver
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(SpiderBridge)
    process.start()