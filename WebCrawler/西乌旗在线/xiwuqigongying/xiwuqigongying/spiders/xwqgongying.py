import datetime
import re

import scrapy
from ..items import XiwuqigongyingItem


class XwqgongyingSpider(scrapy.Spider):
    name = 'xwqgongying'
    allowed_domains = ['www.xwq.ccoo.cn/']

    # start_urls = ['http://www.xwq.ccoo.cn//']

    def start_requests(self):
        item = XiwuqigongyingItem()
        for meatName in ['牛肉', '羊肉']:
            url = 'http://www.xwq.ccoo.cn/post/shenghuo/search/?key={}'.format(meatName)
            headers = {
                'Cookie': 'ccooid=siteid=; UM_distinctid=17b8bdb043355a-028b6b43c807ce-6c507c2e-1fa400-17b8bdb0434b83; siteid=2632; sitename=%e8%a5%bf%e4%b9%8c%e6%97%97%e5%9c%a8%e7%ba%bf; CNZZDATA3834609=cnzz_eid%3D103927693-1630131962-%26ntime%3D1630283179; ASP.NET_SessionId=p01dlb3yhukyqpeelylkcaoi',
                'Host': 'www.xwq.ccoo.cn',
                'Pragma': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
            }
            item['meatName'] = meatName
            yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True, meta={'item': item})

    def parse(self, response):
        item = response.meta['item']
        li_list = response.xpath('//ul[@class="ser_list_ul"]//li')
        for eve_li in li_list:
            item['title'] = eve_li.xpath('.//h6/a/span[@class="txt-f"]/text()')[0].extract()
            item['phone'] = eve_li.xpath('.//div[@class="r"]/p/text()')[0].extract().strip()
            item['company'] = eve_li.xpath('.//h6/a/span[@class="txt-f"]/text()')[0].extract()
            item['contact'] = eve_li.xpath('.//h6/a/span[@class="txt-f"]/text()')[0].extract()
            url = 'http://www.xwq.ccoo.cn' + eve_li.xpath('.//h6/a/@href')[0].extract()
            headers = {
                "Referer": "http://www.xwq.ccoo.cn/post/shenghuo/search/?key=%E7%89%9B%E8%82%89",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36",
            }

            # item['cur_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield scrapy.Request(url=url, headers=headers, dont_filter=True, callback=self.parse1, meta={"item": item})

    def parse1(self, response):
        item = response.meta["item"]
        # 发布时间
        pattern = re.compile('发布时间：(\d{4}-\d{2}-\d{2}) ')
        publishTime = response.xpath('//span[@class="fltl"]/text()')[0].extract()
        item['publishTime'] = re.findall(pattern=pattern, string=publishTime)[0]
        # 插入时间
        item['cur_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield item
