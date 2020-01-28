# -*- coding: utf-8 -*-
import json

from crawlerPython.hadoop_explorer import HadoopWebExplorer
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

folder_name = 'kolesa'
file_name = 'cars.json'

class JsonWriterPipeline(object):
    # def process_item(self, item, spider):
    # 	item['brand'] = item['brand'].upper()
    # 	item['city'] = item['city'].upper()
    #     return item

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        hadoop_explorer = HadoopWebExplorer()
        line = json.dumps(dict(item)) + "\n"
        #self.file.write(line)
        hadoop_explorer.write_to_file(folder_name, file_name, line, append=True)
        return item