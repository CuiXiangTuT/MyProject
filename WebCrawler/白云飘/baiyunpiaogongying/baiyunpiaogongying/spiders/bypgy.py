import datetime

import scrapy
from ..items import BaiyunpiaogongyingItem


class BypgySpider(scrapy.Spider):
    name = 'bypgy'
    allowed_domains = ['http://www.nmlpw.com']

    # start_urls = ['http://http://www.nmlpw.com//']

    def start_requests(self):
        item = BaiyunpiaogongyingItem()
        for meat_name in ['牛肉', '羊肉']:
            start_url = 'http://www.nmlpw.com/index.php?mod=product&act=list&keyword={}'.format(meat_name)
            headers = {
                'Referer': 'http://www.nmlpw.com/index.php?mod=product&act=list&keyword=%E7%89%9B%E8%82%89',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                'Cookie': 'PHPSESSID=9lqhraanc0r00ek40ob0nov3m2; Hm_lvt_161ef4a6d10f86bc9955e58edf1a0462=1629766122,1629766489,1629775651,1630031420; nb-referrer-hostname=www.nmlpw.com; Hm_lpvt_161ef4a6d10f86bc9955e58edf1a0462=1630124671; nb-start-page-url=http%3A%2F%2Fwww.nmlpw.com%2Findex.php%2Farticle%2F14'
            }
            item['meat_kind'] = meat_name
            yield scrapy.Request(url=start_url, headers=headers, callback=self.parse, dont_filter=True,
                                 meta={'item': item})

    def parse(self, response):
        produce_list = response.xpath('..//div[@class="prolist_html"]//div[@class="prolist"]')
        item = response.meta['item']
        for eve_product in produce_list:
            # 产品名
            item['prolist_name'] = eve_product.xpath('.//p[@class="prolist_name"]/text()')[0].extract()
            # 价格
            item['price'] = eve_product.xpath('.//span[contains(@class,"money1") and contains(@class,"fl")]/text()')[
                0].extract()
            # 联系人
            item['contact'] = '北京市大草原蒙特食品贸易有限公司'
            # 联系电话
            item['phone'] = '4006171039'
            # 联系电话1
            item['phone1'] = '01084046682'
            # 联系电话2
            item['phone2'] = '64053870'
            # 插入时间
            item['cur_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
