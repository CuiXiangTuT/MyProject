import json
from datetime import datetime

import scrapy


class DpygcgyxSpider(scrapy.Spider):
    name = 'dpygcgyx'
    allowed_domains = ['www.cciinet.com']
    start_urls = ['http://www.cciinet.com/']

    def start_requests(self):
        url = 'https://m.cciinet.com/shopapi/shopSupplyDemand/findSupplyDemandList'
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.296297)",
            "Content-Type": "application/json",
            # "Content-Length":"192",
            "Host": "m.cciinet.com",
            # "Connection":"Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=AA3A2B6E98C8D4D0337D7C7597E16F9E; route=9274099c1cbbe0919517fead30b30098",
        }
        for word in ['牛', '羊']:
            for i in range(1, 200):
                data_json = {"page": {"current": i, "size": 15, "desc": ["create_date"]},
                             "shopSupplyDemand": {"goodsCategory": word, "goodsType": "-1", "origin": None,
                                                  "provinceId": None, "type": 1, "isOpenPayment": None,
                                                  "userId": 48954}}
                data = json.dumps(data_json)

                yield scrapy.Request(url=url, headers=headers, method='POST', body=data, dont_filter=True,
                                     callback=self.parse)

    def parse(self, response):
        json_data = response.json()['data']['records']
        item = {}
        for eve_data in json_data:
            # 产品
            item['title'] = eve_data['title']
            # 分类
            item['goodsCategory'] = eve_data['goodsCategory']
            # 意向产地
            item['origin'] = eve_data['origin']
            # 收货省份id
            item['provinceId'] = eve_data['provinceId']
            # 收货省份
            item['provinceName'] = eve_data['provinceName']
            # 收货城市id
            item['cityId'] = eve_data['cityId']
            # 收货城市
            item['cityName'] = eve_data['cityName']
            # 联系方式
            item['contactsPhone'] = eve_data['contactsPhone']
            # 采购数量
            item['goodsAmount'] = eve_data['goodsAmount']
            # 采购数量单位
            item['priceType'] = eve_data['priceType']
            # 意向价格：-1：面议
            if item['priceType']:
                item['priceTypeDetail'] = '面议'
            else:
                item['priceTypeDetail'] = ''

            # 意向价格
            item['goodsPrice'] = eve_data['goodsPrice']
            # 采购要求
            item['details'] = eve_data['details']
            # 创建时间
            item['update_Date'] = eve_data['updateDate']
            # 公司id
            item['companyId'] = eve_data['companyId']
            # 用户id
            item['userId'] = eve_data['userId']
            url = 'https://m.cciinet.com/shopapi/shopSupplyDemand/findSupplyDemandDetail?id={}&userId={}'.format(
                eve_data['id'], eve_data['userId'])
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.296297)",
                "Host": "m.cciinet.com",
                "Connection": "Keep-Alive",
                # "Accept-Encoding": "gzip",
                "Cookie": "JSESSIONID=911AB8E253A6735194EF4789280229EF; route=9274099c1cbbe0919517fead30b30098; acw_tc=71e5fc9b16294505995125685ede4fe56de0a24d00a9fb5cf150ecb643",
            }
            yield scrapy.Request(url=url, headers=headers, dont_filter=True, callback=self.parse1, meta={'item': item})

    def parse1(self, response):
        json_data = response.json()['data']['shopSupplyDemand']
        item = response.meta['item']
        # 要求：-1：不限 0：现货
        item['goodsType'] = json_data['goodsType']
        if item['goodsType']:
            item['goodsTypeRequirement'] = '不限'
        else:
            item['goodsTypeRequirement'] = '现货'
        # 公司名称
        item['companyName'] = response.json()['data']['company']['companyName']
        # 公司地址
        item['address'] = response.json()['data']['company']['address']
        # 入库时间
        item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield item
