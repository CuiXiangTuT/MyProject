import datetime

import scrapy
from ..items import ShihaomuyegongyingItem

class ShmygySpider(scrapy.Spider):
    name = 'shmygy'
    allowed_domains = ['http://www.nmgshsy.com/']

    # start_urls = ['http://http://www.nmgshsy.com//']

    def start_requests(self):
        for pageNum in range(1, 8):
            url = 'http://www.nmgshsy.com/list/7?id=7&page={}'.format(pageNum)
            headers = {
                'Referer': 'http://www.nmgshsy.com/list/7?id=7&page=1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
            }
            yield scrapy.Request(url=url,headers=headers,dont_filter=True,callback=self.parse)


    def parse(self, response):
        item = ShihaomuyegongyingItem()
        dlList = response.xpath('//div[@class="leftnav-z1-list"]//dl')
        for perDl in dlList:
            # 产品名
            item['title'] = perDl.xpath('.//h4/a/text()')[0].extract()
            # 电话
            item['phone'] = '15849244446'
            # 联系人
            item['contact'] = '张先生'
            # 电话2
            item['standbyPhone'] = '0472-8800338'
            # 邮箱
            item['email'] = '1127837509@.qq.com'
            # 插入时间
            item['curTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
