import datetime
import re
from ..items import ShipinzixunzhongxinItem
import scrapy
from lxml import etree

class SpzxzxSpider(scrapy.Spider):
    name = 'spzxzx'
    allowed_domains = ['http://news.foodmate.net/']

    # start_urls = ['http://http://news.foodmate.net//']
    def start_requests(self):
        item = ShipinzixunzhongxinItem()
        for meatName in ['牛肉', '羊肉']:
            for pageNum in range(1, 41):
                url = 'http://news.foodmate.net/search.php?moduleid=21&spread=0&kw={}&page={}'.format(meatName, pageNum)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36'
                }
                item['meatName'] = meatName
                yield scrapy.Request(url=url,headers=headers,callback=self.parse,dont_filter=True,meta={'item':item})

    def parse(self, response):
        item = response.meta['item']
        newsUrlList = response.xpath('//li[@class="catlist_li"]//a/@href').extract()
        for perUrl in newsUrlList:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36'
            }
            yield scrapy.Request(url=perUrl,headers=headers,callback=self.parse1,dont_filter=True,meta={'item':item})


    def parse1(self,response):
        item = response.meta['item']
        try:
            # 标题
            item['title'] = response.xpath('//h1[@class="title"]/text()')[0].extract()
        except:
            item['title'] = ''
        # 作者
        try:
            # 作者
            item['author'] = re.findall(re.compile('作者：(.*?)&nbsp'),response.body.decode(response.encoding))[0]
        except:
            # 作者
            item['author'] = ''
        # 时间
        try:
            # 时间
            item['creationTime'] = re.findall(re.compile('时间：(.*?)&nbsp'),response.body.decode(response.encoding))[0]
        except:
            # 时间
            item['creationTime'] = ''
        # 来源
        try:
            # 来源
            item['newsSource'] = re.findall(re.compile('来源：(.*?)&nbsp'),response.body.decode(response.encoding))[0]
        except:
            # 来源
            item['newsSource'] = ''
        # 核心提示
        try:
            # 核心提示
            item['coreTips'] = response.xpath('//div[@class="introduce"]/text()')[0].extract()
        except:
            # 核心提示
            item['coreTips'] = ''
        try:
            # 正文
            responseE = etree.HTML(response.text)
            content = responseE.xpath('//div[@class="content"]')[0]
            a_pattern = re.compile('href="(.*?)"')
            contentString = etree.tostring(content, encoding="utf-8").decode('utf-8')
            try:
                aList = re.findall(a_pattern, contentString)
                if contentString:
                    for k in aList:
                        contentString = contentString.replace(k, 'javascript:;').replace('<a','<span').replace('/a>','/span>')
                item['content'] = contentString
            except:
                item['content'] = contentString
            # 插入时间
            item['cur_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # print(item)
            yield item
        except:
            pass

