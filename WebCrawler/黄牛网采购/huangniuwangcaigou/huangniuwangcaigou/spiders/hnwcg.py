import scrapy
from ..items import HuangniuwangcaigouItem

class HnwcgSpider(scrapy.Spider):
    name = 'hnwcg'
    allowed_domains = ['http://www.chinahuangniu.com/']

    # start_urls = ['http://http://www.chinahuangniu.com//']

    def start_requests(self):
        for i in range(1, 20):
            start_url = 'http://www.chinahuangniu.com/portal-api/pendingOrder/platform/supply/getCustPage?pageSize=20&pageNum=' + str(
                i) + '&minUnitPrice=&placeCity=&maxUnitPrice=&totalCount=0&endingDate=&placeProvince=&placeArea='
            headers = {
                "Referer": "http://www.chinahuangniu.com/html/buy/supplyList.html",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
            }
            yield scrapy.Request(url=start_url, headers=headers, dont_filter=True, callback=self.parse)

    def parse(self, response):
        json_data_list = response.json()['data']['list']
        item = HuangniuwangcaigouItem()
        for eve_data in json_data_list:
            # 产品id
            item['goodsId'] = eve_data['id']
            # 产品名
            item['goodsName'] = eve_data['goodsName']
            # 最低价
            item['minUnitPrice'] = eve_data['minUnitPrice']
            # 最高价
            item['maxUnitPrice'] = eve_data['maxUnitPrice']
            # 数量
            item['totalCount'] = eve_data['totalCount']
            # 单位
            item['goodsUnit'] = eve_data['goodsUnit']
            # 截止日期
            item['endingDate'] = eve_data['endingDate']
            # 品种
            item['title'] = eve_data['title']
            # 原产地
            item['placeAll'] = eve_data['placeAll']
            yield item


