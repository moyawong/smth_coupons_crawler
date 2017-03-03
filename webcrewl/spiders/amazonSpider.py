# -*- coding: utf-8 -*-
import scrapy
from webcrewl.items import CouponItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as EC
from bs4 import BeautifulSoup
from scrapy import signals
from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher
from webcrewl.platform import getPlatform
from webcrewl.emails import send_mail

class amazonSpider(scrapy.spiders.CrawlSpider):

    name="amz"
    base_url = settings['AM_BASE_URL']
    start_urls = [base_url]
#    start_urls.extend([settings['AMZ_PAGE_URL']])
    print start_urls
    
    platform = getPlatform()

    def __init__(self):
        scrapy.spiders.Spider.__init__(self)
        self.driver = webdriver.PhantomJS()
            
        self.driver.set_page_load_timeout(15)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.quit()

    def parse(self,response):
        print "parsing::::::::::::::::::::::::::"
        self.driver.get(response.url)
        print response.url
        
#         try:
#             
#             element = WebDriverWait(self.driver,30).until(
#                 EC.presence_of_all_elements_located((By.ID, 'widgetContent'))
#             )
#             print 'element:\n', element
#         except Exception, e:
#             print Exception, ":", e
#             print "wait failed"

        self.driver.implicitly_wait(20)
        myelement = self.driver.find_element_by_id("widgetContent")
        print("element = ", myelement)
            
        page_source = self.driver.page_source
        bs_obj = BeautifulSoup(page_source, "lxml")
        print bs_obj

#        table = bs_obj.find('table',class_='board-list tiz')
#        print table
        
        print "find message ====================================\n"
        coupon_messages = bs_obj.find_all('span', class_='a-declarative')
        count = 0
        for message in coupon_messages:
            print("messages = %s"%message)
            count += 1
            
        print("sum count = ", count)

        
    def canCreateItem(self, title):
        for key in settings['KEYS']:
            if key in title:
                return True      
        return False

    def parse_content(self,url):
        
        try:
            self.driver.get(url)
        except Exception,e:
            print "give up one detail"
            return ""
        
        try:
            element = WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.ID, 'a-row dealTile'))
            )
            print 'element:\n', element
        except Exception, e:
            print Exception, ":", e
            print "wait failed"
            
        page_source = self.driver.page_source
        bs_obj = BeautifulSoup(page_source, "lxml")
        
        return '%s'%bs_obj.find('td', class_='a-content').p.get_text().encode('utf-8','ignore')
    
