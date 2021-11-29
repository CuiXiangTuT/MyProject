import scrapy
from pprint import pprint
from ..items import RoupinhuigongyingItem
from datetime import datetime

class RphgySpider(scrapy.Spider):
    name = 'rphgy'
    allowed_domains = ['www.roupinhui.com']

    # start_urls = ['http://www.roupinhui.com/']

    def start_requests(self):
        start_urls = 'https://portal.roupinhui.net/product/getLevelTwoProduct?parentId=0&__t=1625815725279'
        yield scrapy.Request(url=start_urls, dont_filter=True, callback=self.parse)

    def parse(self, response):
        json_data = response.json()["data"]

        item = RoupinhuigongyingItem()
        # 供应
        item['buy_supply'] = '供应'
        # 数据来源
        item['data_source'] = "肉品汇"

        # 定义空的列表用于存放羊产品
        sheep_list = []
        # 定义空的列表用于存放牛产品
        ox_list = []
        # 定义一个空的列表用于存放羊产品和牛产品的列表
        zonghe = []

        for i in json_data:
            if i['parentId'] == 2:
                ox_list.append(i)
            if i['parentId'] == 3:
                sheep_list.append(i)
        zonghe.append(ox_list)
        zonghe.append(sheep_list)

        for k in zonghe:
            if k == 0:
                item['meat_name'] = "牛产品"
            else:
                item['meat_name'] = "羊产品"
            for j in k:
                url = 'https://portal.roupinhui.net/supply/search?parentId=' + str(j['parentId']) + '&productId=' + str(
                    j['id']) + '&pageSize=15&pageNum=1&type=-1&__t=1625816804503'
                yield scrapy.Request(url=url, callback=self.parse1, dont_filter=True, meta={'item': item})

    def parse1(self, response):
        item = response.meta['item']
        json_data = response.json()["data"]
        for i in json_data:
            # 产品名称
            item['productName'] = i['productName']
            # 产地
            item["placeOrigin"] = i['placeOrigin']
            # 工厂号
            item['factoryNm'] = i['factoryNm']
            # 联系人
            item['realName'] = i['realName']
            # 电话
            item['phone'] = i['phone']
            # 更新时间
            item['releaseTime'] = i['releaseTime']
            # 最新时间
            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pprint(item)
            return item
