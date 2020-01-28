from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPython.items import KolesaItem
import urllib.request
import json


class KolesaSpider(CrawlSpider):
    name = "KolesaSpider"
    allowed_domains = ["kolesa.kz"]
    rules = (
        Rule(LinkExtractor(allow=('.+kolesa.kz/a/show.+'), deny=('.+kolesa.kz/cars/.+')), callback='parse_page'),   # TODO: вот тут надо подумать
        #Rule( callback='parse_page'),
    )
    #start_urls = ['https://kolesa.kz/cars/']
    
    def __init__(self, *a, **kw):
        super(KolesaSpider, self).__init__(*a, **kw)
        urls = []

        for i in range(101697811,101697814):
            
            url = 'https://kolesa.kz/a/show/' + str(i)
            
            if i%1000==0:
                print(i)
            try:
                f = urllib.request.urlopen(url)
                print(url)
                urls.append(url)
            except:
                print(url)
                print('not found')
                pass
        self.start_urls = urls


    def checkelement(self, lst):
        if len(lst)>0:
            return lst[0].strip()
        return ''


    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse_page(self, response):
        print('-----parse_page-----')
        urlT = 'https://kolesa.kz/a/ajaxPhones/?id='
        root = Selector(response)
        item = KolesaItem()
        if self.checkelement(root.xpath("//ol/li/a[@href = '/cars/']/text()").extract()) == 'Легковые':
            item['idCar'] = response.url #self.checkelement(root.xpath("//link[@rel='canonical']/@href").extract())
            item['brand'] = self.checkelement(root.xpath("//h1[@class='offer__title']/span[@itemprop='brand']/text()").extract())
            
            req = urllib.request.Request(urlT + response.url[25:])
            req.add_header('x-requested-with', 'XMLHttpRequest')
            phones = []
            try:
                resp = urllib.request.urlopen(req)
                phones = json.loads(resp.read())["phones"]
            except:
                phones = []

            item['phones'] = phones
            item['name'] = self.checkelement(root.xpath("//h1[@class='offer__title']/span[@itemprop='name']/text()").extract())
            item['year'] = self.checkelement(root.xpath("//h1[@class='offer__title']/span[@class='year']/text()").extract())
            item['city'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Город']/../../dd/text()").extract())
            item['body'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Кузов']/../../dd/text()").extract())
            item['volume'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Объем двигателя, л']/../../dd/text()").extract())
            item['mileage'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Пробег']/../../dd/text()").extract())
            item['transmission'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Коробка передач']/../../dd/text()").extract())
            item['rudder'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Руль']/../../dd/text()").extract())
            item['color'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Цвет']/../../dd/text()").extract())
            item['driveUnit'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Привод']/../../dd/text()").extract())
            item['disinhibited'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Растаможен']/../../dd/text()").extract())
            #item['comments'] = 
            yield item