from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawlerPython.items import KolesaItem
import urllib.request


class KolesaSpider(CrawlSpider):
    name = "KolesaSpider"
    allowed_domains = ["kolesa.kz"]
    rules = (
        Rule( callback='parse_page'),   # TODO: вот тут надо подумать
    )
    start_urls = ['https://kolesa.kz/cars/']
    
    # def __init__(self, *a, **kw):
    #     super(KolesaSpider, self).__init__(*a, **kw)
    #     urls = []
    #     for i in range(99399988,99399998):
    #         url = 'https://kolesa.kz/a/show/' + str(i)
    #         if i%1000==0:
    #             print(i)
    #         try:
    #             f = urllib.request.urlopen(url)
    #             print(url)
    #             urls.append(url)
    #         except:
    #             pass
    #     self.start_urls = urls


    def checkelement(self, lst):
        if len(lst)>0:
            return lst[0].strip()
        return ''


    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse_page(self, response):
        print('-----parse_page-----')
        root = Selector(response)
        item = KolesaItem()
        if self.checkelement(root.xpath('/html/body/main/div/div/div[2]/div/ol/li[2]/a/text()').extract()) == 'Легковые':
            item['idCar'] = self.checkelement(root.xpath("//link[@rel='canonical']/@href").extract())
            item['brand'] = self.checkelement(root.xpath("//h1[@class='offer__title']/span[@itemprop='brand']/text()").extract())
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
            #item['comments'] = self.checkelement(root.xpath("//dl/dt/span[text() = 'Растаможен']/../../dd/text()").extract())
            yield item
        pass