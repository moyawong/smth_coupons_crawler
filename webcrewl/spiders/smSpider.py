#coding=utf-8
import time
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

class SMSpider(scrapy.spiders.CrawlSpider):
    '''
    #要建立一个 Spider，你可以为 scrapy.spider.BaseSpider 创建一个子类，并确定三个主要的、强制的属性：
    #name ：爬虫的识别名，它必须是唯一的，在不同的爬虫中你必须定义不同的名字.
    #start_urls ：爬虫开始爬的一个 URL 列表。爬虫从这里开始抓取数据，所以，第一次下载的数据将会从这些 URLS 开始。其他子 URL 将会从这些起始 URL 中继承性生成。
    #parse() ：爬虫的方法，调用时候传入从每一个 URL 传回的 Response 对象作为参数，response 将会是 parse 方法的唯一的一个参数,
    #这个方法负责解析返回的数据、匹配抓取的数据(解析为 item )并跟踪更多的 URL。
    '''
    name="sm"
    base_url = settings['BASE_URL']
    start_urls = [base_url]
#    start_urls.extend([base_url+'?p='+str(i) for i in range(2,50)])
    start_urls.extend([base_url+'?p='+str(i) for i in xrange(2,3)])
    print start_urls
    # start_urls = ['http://www.newsmth.net/']
    platform = getPlatform()

    def __init__(self):
        scrapy.spiders.Spider.__init__(self)
        self.driver = webdriver.PhantomJS()
            
        self.driver.set_page_load_timeout(15)
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def __del__(self):
    #     print '__del__ running'
    #     self.driver.quit()

    def spider_closed(self, spider):
        self.driver.quit()

    #具体爬虫function
    def parse(self,response):
        print "parsing::::::::::::::::::::::::::"
        self.driver.get(response.url)
        print response.url
        
        try:
            element = WebDriverWait(self.driver,30).until(
                EC.presence_of_all_elements_located((By.TAG_NAME,'table'))
            )
            print 'element:\n', element
        except Exception, e:
            print Exception, ":", e
            print "wait failed"
            
        page_source = self.driver.page_source
        bs_obj = BeautifulSoup(page_source, "lxml")
        print bs_obj
        
        table = bs_obj.find('table',class_='board-list tiz')
        print table
        
        print "find message ====================================\n"
        intern_messages = table.find_all('tr',class_=False)
        for message in intern_messages:
            title, href, smtime, author = '','','',''
            td_9 = message.find('td',class_='title_9')
            if td_9:
                title = td_9.a.get_text().encode('utf-8','ignore')
                href = td_9.a['href']
                
            if not self.canCreateItem(title):
                continue
                
            td_10 = message.find('td', class_='title_10')
            if td_10:
                smtime=td_10.get_text().encode('utf-8','ignore')
                
            td_12 = message.find('td', class_='title_12')
            if td_12:
                author = td_12.a.get_text().encode('utf-8','ignore')
                
            item = CouponItem()
            print 'title:',title
            print 'href:', href
            print 'time:', smtime
            print 'author:', author
            item['title'] = title
            item['href'] = href
            item['time'] = smtime
            item['author'] = author
            item['dbtime'] = time.strftime("%Y-%m-%d", time.localtime()) 
            item['base_url_index'] = 0
            root_url = settings['ROOT_URL']
            # content = scrapy.Request(root_url+href,self.parse_content)
            if href!='':
                content = self.parse_content(root_url+href)
                # print 'content:', content
                item['content'] = content
            
            yield item
            
        # intern_messages = response.xpath('//table[@class="board-list tiz"]')
        # print intern_messages
        # for intern_message in intern_messages:
        #     title = intern_message.xpath('/td[@class="title_9"]/a').text()
        #     print title
        
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
                EC.presence_of_all_elements_located((By.TAG_NAME, 'table'))
            )
            print 'element:\n', element
        except Exception, e:
            print Exception, ":", e
            print "wait failed"
            
        page_source = self.driver.page_source
        bs_obj = BeautifulSoup(page_source, "lxml")
        
        return '%s'%bs_obj.find('td', class_='a-content').p.get_text().encode('utf-8','ignore')
    
