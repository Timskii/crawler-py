# -*- coding: utf-8 -*-
import json
import pymongo
from crawlerPython.mongo import db




#from crawlerPython.hadoop_explorer import HadoopWebExplorer
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class KolesaPipeline(object):
    
    def process_item(self, item, spider):

        collection = db.kolesa
        valid = True
        for data in item:
            if not data:
                valid = False
                print("Missing {0}!".format(data))
        if valid:
            collection.insert(dict(item))
            print("Question added to MongoDB database!")
        return item