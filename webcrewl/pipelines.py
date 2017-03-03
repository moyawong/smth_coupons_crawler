# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log
from webcrewl.emails import send_mail

class MongoDBPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data :
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if item['title'] == '':
            valid = False
            raise DropItem("title is empty")
        if item['content'] == '':
            valid = False
            raise DropItem("content is empty")
        
        for keyword in settings['EXCLUDE']:
            if keyword in item['title']:
                valid = False
                DropItem("title have invalid keywords")
                break
        
        if valid:
            iskey = False
            for key in settings['KEYS']:
                if key in item['title']:
                    iskey = True
                    break
            for author in settings['AUTHOR']:
                if author == item['author']:
                    iskey = True
                    break
            if not iskey:
                raise DropItem("item do not have keywords")
            
            for info in self.db.items.find({}, {"title":1}):
                infoTitle = info["title"].encode("utf-8")
                if infoTitle == item["title"]:
                    valid = False
                    raise DropItem("item exist!")
                    break
            
        if valid:
            self.collection.insert(dict(item))
            send_mail(item['title'], item['content'], item['href'])
            
            # log.msg("webCrewl item added to MongoDB database!",
            #         level=log.DEBUG, spider=spider)
        return item

class TagPipeline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
#        self.getTags(item)
        
        return item

    def getTags(self,item):
        text = item['title']
        is_key = False
        for key in settings['KEYS']:
            if key in text:
                is_key = True
                break

        item['is_key'] = is_key
