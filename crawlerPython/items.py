# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KolesaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    idCar = scrapy.Field()	#url
    phones = scrapy.Field() # phones
    brand = scrapy.Field()	#марка
    name = scrapy.Field()	#модель
    year = scrapy.Field()	#год
    city = scrapy.Field()	#город
    body = scrapy.Field()	#кузов
    volume = scrapy.Field()	#объем
    mileage = scrapy.Field()	#пробег
    transmission = scrapy.Field()	#кпп
    rudder = scrapy.Field()	#руль
    color = scrapy.Field()	#цвет
    driveUnit = scrapy.Field()	#привод
    disinhibited = scrapy.Field() #расторможен
    comments = scrapy.Field() #коментарии
    _id = ""

