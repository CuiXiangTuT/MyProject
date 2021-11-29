import json
from datetime import datetime
from ..items import BeijingxinfadixinxizhongxinItem

import scrapy


class BjxfdxxzxSpider(scrapy.Spider):
    name = 'bjxfdxxzx'
    allowed_domains = ['http://www.xinfadi.com.cn/']


    def start_requests(self):
        zipList = list(zip(['牛肉类', '羊肉类'], [32, 36]))
        item = BeijingxinfadixinxizhongxinItem()
        for zipIndex in range(len(zipList)):
            for pageNum in range(1, zipList[zipIndex][1] + 1):
                item['meatSort'] = zipList[zipIndex][0]
                if zipList[zipIndex][0] == '牛肉类':
                    prodCatid = '1206'
                else:
                    prodCatid = '1207'
                url = 'http://www.xinfadi.com.cn/getPriceData.html?limit=20&current={}&pubDateStartTime=&pubDateEndTime=&prodPcatid=1189&prodCatid={}&prodName='.format(
                    pageNum, prodCatid)
                headers = {
                    'Referer': 'http://www.xinfadi.com.cn/priceDetail.html',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                }
                yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True,
                                     meta={'item': item}, method='POST')

    def parse(self, response):
        jsonDataList = response.json()['list']
        item = response.meta['item']
        print(jsonDataList)
        for perJsonData in jsonDataList:
            # 品名id
            item['prodID'] = perJsonData['id']
            # 一级分类
            item['primaryClassification'] = perJsonData['prodCat']
            # 二级分类
            item['secondaryClassification'] = perJsonData['prodPcat']
            # 品名
            item['prodName'] = perJsonData['prodName']
            # 最低价
            item['lowPrice'] = perJsonData['lowPrice']
            # 平均价
            item['avgPrice'] = perJsonData['avgPrice']
            # 最高价
            item['highPrice'] = perJsonData['highPrice']
            # 规格
            item['specifications'] = perJsonData['specInfo']
            # 产地
            item['place'] = perJsonData['place']
            # 单位
            item['unitInfo'] = perJsonData['unitInfo']
            # 发布日期
            item['pubDate'] = perJsonData['pubDate']
            # 插入日期
            item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
