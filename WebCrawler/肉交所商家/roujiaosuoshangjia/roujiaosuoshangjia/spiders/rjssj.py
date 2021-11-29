from datetime import datetime

import scrapy
from ..items import RoujiaosuoshangjiaItem


class RjssjSpider(scrapy.Spider):
    name = 'rjssj'
    allowed_domains = []

    def start_requests(self):
        url = 'http://www.roujiaosuo.com/mobile/market_list.php'
        for i in range(1, 200):
            data = {
                "action": "list",
                "origin": "116.2529,39.5420",
                "city": "北京市",
                "page": str(i),
            }

            yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse, dont_filter=True)

    def parse(self, response):
        try:
            res_data_list = response.json()['data']
            item = RoujiaosuoshangjiaItem()
            for res_data in res_data_list:
                item['title'] = res_data['title']
                item['address'] = res_data['address']
                item['coordinate'] = res_data['longlat']
                item['itemid'] = res_data['itemid']
                item['shop_num'] = res_data['shopnum']
                index_url = 'http://www.roujiaosuo.com/mobile/company_api.php'
                for i in range(1, (int(res_data['shopnum']) // 10) + 2):
                    data = {
                        "action": "list",
                        "itemid": str(item['itemid']),
                        "origin": "116.2529,39.5420",
                        "city": "北京市",
                        "page": str(i),
                    }
                    yield scrapy.FormRequest(url=index_url, formdata=data, dont_filter=True, callback=self.parse1,
                                             meta={'item': item})
        except:
            pass
        # else:
        #     self.crawler.engine.close_spider(self, '已经没有数据，爬虫终止~')

    def parse1(self, response):
        item = response.meta['item']
        res_data_list = response.json()['data']
        for i in res_data_list:
            item['username'] = i['username']
            item['company'] = i['company']
            item['business_addr'] = i['address']
            item['business'] = i['business']
            item['longlat'] = i['longlat']
            item['truename'] = i['truename']
            item['areaid'] = i['areaid']
            item['street'] = i['street']
            url = 'http://www.roujiaosuo.com/mobile/shop_api.php'
            data = {
                "action": "index",
                "token": "",
                "username": item['username'],
            }
            yield scrapy.FormRequest(url=url, formdata=data, dont_filter=True, callback=self.parse2,
                                     meta={'item': item})

    def parse2(self, response):
        item = response.meta['item']
        json_data = response.json()['data']['info']
        item['phone'] = json_data['mobile']
        item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(item)
        yield item
