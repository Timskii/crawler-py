# -*- coding: utf-8 -*-
import json
import pymongo




#from crawlerPython.hadoop_explorer import HadoopWebExplorer
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class JsonWriterPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            host= '192.168.1.208',
            port= 27017,
            username= 'u',
            password= 'u123',
            authSource= 'crawlers'
        )
        db = connection.crawlers
        self.collection = db.kolesa


    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                print("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            print("Question added to MongoDB database!")
        return item