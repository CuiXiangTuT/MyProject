import json
from datetime import datetime
import emoji
import scrapy
from ..items import DongpinyigangshanghudatingItem


class DpygshdtSpider(scrapy.Spider):
    name = 'dpygshdt'
    allowed_domains = ['www.cciinet.com']

    # start_urls = ['http://www.cciinet.com/']

    def start_requests(self):
        url = 'https://m.cciinet.com/shopapi/shopSupplyDemand/findSupplyDemandList'
        headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.296297)",
            "Content-Type": "application/json",
            # "Content-Length": "192",
            "Host": "m.cciinet.com",
            # "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "Cookie": "JSESSIONID=449150105293B34160DAB5438A496BE9; route=9274099c1cbbe0919517fead30b30098; acw_tc=71e5fc9916294287975996404e4055ec469f41293574fd5f401ae2bbb5",
        }
        key_word = ['牛', '羊']
        for word in key_word:
            for i in range(400):
                data_json = {"page": {"current": i, "size": 99, "desc": ["create_date"]},
                             "shopSupplyDemand": {"goodsCategory": word, "goodsType": "-1", "origin": None,
                                                  "provinceId": None,
                                                  "type": 0, "isOpenPayment": None, "userId": 48954}}
                data = json.dumps(data_json)

                yield scrapy.Request(url=url, headers=headers, method='POST', body=data, dont_filter=True,
                                     callback=self.parse)

    def parse(self, response):
        try:
            # print(response.json()["data"]['records'])
            data_total_list = response.json()["data"]['records']
            item = DongpinyigangshanghudatingItem()
            for eve_data in data_total_list:
                # 上传时间
                item['update_time'] = eve_data['updateDate']
                # 包装规格
                item['packageUnit'] = eve_data['packageUnit']
                # 产地(国家)
                item['origin'] = eve_data['origin']
                # 公司
                item['companyName'] = eve_data['companyName']
                # 类别
                item['goodsCategory'] = eve_data['goodsCategory']
                # 数量
                item['goodsAmount'] = eve_data['goodsAmount']
                # 是否公开支付
                item['isOpenPayment'] = eve_data['isOpenPayment']
                # 厂号
                item['factoryNo'] = eve_data['factoryNo']
                # 城市id
                item['cityId'] = eve_data['cityId']
                # 产品
                item['title'] = emoji.emojize(emoji.demojize(eve_data['title']))
                # 等级
                item['memberGradeId'] = eve_data['memberGradeId']
                # 城市名字
                item['cityName'] = eve_data['cityName']
                # 单位id
                item['unitId'] = eve_data['unitId']
                # id
                item['u_id'] = eve_data['id']
                # 单位名称
                item['unitName'] = eve_data['unitName']
                # 省份id
                item['provinceId'] = eve_data['provinceId']
                # 用户id
                item['userId'] = eve_data['userId']
                # 规格值
                item['specificationValue'] = eve_data['specificationValue'][0]['value']
                # 公司id
                item['companyId'] = eve_data['companyId']
                # 产品号
                item['productCode'] = eve_data['productCode']
                # 是否置顶
                item['isTop'] = eve_data['isTop']
                # 产品价格
                item['goodsPrice'] = str(eve_data['goodsPrice']) + '/' + eve_data['unitName']
                # 省份
                item['provinceName'] = eve_data['provinceName']

                url = 'https://m.cciinet.com/shopapi/shopSupplyDemand/findSupplyDemandDetail?id={}&userId={}'.format(
                    eve_data['id'], eve_data['userId'])
                headers = {
                    "user-agent": "Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.296297)",
                    "Host": "m.cciinet.com",
                    # "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "Cookie": "JSESSIONID=AA3A2B6E98C8D4D0337D7C7597E16F9E; route=9274099c1cbbe0919517fead30b30098; acw_tc=71e5fc9b16294387275358895e4e54251ef922791efd9e2e26eeb61f21",
                }
                yield scrapy.Request(url=url, headers=headers, dont_filter=True, callback=self.parse1,
                                     meta={'item': item})
        except:
            pass

    def parse1(self, response):
        item = response.meta['item']
        json_data = response.json()['data']
        # 电话
        item['contactsPhone'] = json_data['shopSupplyDemand']['contactsPhone']
        # 公司地址
        item['address'] = json_data['company']['address']
        # 公司信息营业执照
        item['licenseImage'] = json_data['company']['licenseImage']
        # 商家信息
        item['business_name'] = emoji.emojize(emoji.demojize(json_data['user']['name']))
        # 起批量
        item['StartingBatch'] = str(json_data['shopSupplyDemand']['quantity']) + item['unitName']
        # 是否带票
        item['isBill'] = json_data['shopSupplyDemand']['isBill']
        # 入库时间
        item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 供货情况
        item['goodsType'] = json_data['shopSupplyDemand']['goodsType']
        # 供货情况说明
        if item['goodsType']:
            item['goodsTypeDetail'] = item['goodsType']
        else:
            item['goodsTypeDetail'] = '现货'
        yield item
