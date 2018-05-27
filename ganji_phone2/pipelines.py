# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient


class GanjiPhonePipeline(object):
    def open_spider(self, spider):
        client = MongoClient()
        self.collection = client.ganji.ganji_phone
        self.test_job = client.ganji.test_job

    def process_item(self, item, spider):
        if spider.name == 'ganji':
            self.collection.insert(dict(item))
            return item
        elif spider.name == 'job':
            self.test_job.insert(dict(item))
            return item