from datetime import datetime

import scrapy
import re
from ..items import AicaigouhuoyuanItem


class AcghySpider(scrapy.Spider):
    name = 'acghy'
    allowed_domains = ['https://b2b.baidu.com/']

    # start_urls = ['http://www.baidu.com/']

    def start_requests(self):
        for meat in ['įč', 'įžč']:
            for i in range(1, 6):
                start_url = 'https://b2b.baidu.com/s/a?q={}&s=100&o=0&from=search&p={}'.format(meat, i)
                headers = {
                    'Env': 'ANDROID',
                    'x-requested-with': 'XMLHttpRequest',
                    'Client-Version': '2.0.3',
                    'User-Agent': 'aipurchaser/2.0.3',
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'Content-Length': '0',
                    'Host': 'b2b.baidu.com',
                    'Connection': 'Keep-Alive',
                    'Accept-Encoding': 'gzip',
                    'Cookie': 'BAIDUID=D6C2BD7968D369B73083908C30F99777:FG=1; B2B_AB_FCT2=3567441097',
                }
                yield scrapy.Request(url=start_url, headers=headers, method='POST', callback=self.parse,
                                     dont_filter=True)

    def parse(self, response):
        json_data_list = response.json()['data']['productList']
        item = AicaigouhuoyuanItem()
        headers = {
            'Env': 'ANDROID',
            'x-requested-with': 'XMLHttpRequest',
            'Client-Version': '2.0.3',
            'User-Agent': 'aipurchaser/2.0.3',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            # 'Content-Length': '0',
            'Host': 'b2b.baidu.com',
            # 'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'Cookie': 'BAIDUID=D6C2BD7968D369B73083908C30F99777:FG=1; B2B_AB_FCT2=3567441097; BCLID=10717115647590491845; BDSFRCVID=sx-OJeC62lfufjjH2he07kKGQHgV_8JTH6XoGim7I5wHfbOM7P41EG0PEM8g0KAb6oJ7ogKK0mOTHUkF_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tbujoKPXfCP3fP36q4jj-tFshp_X5-RLf57Osl7F5l8-hRRI5tj8MxvXMM_jt-ni3a670MQ7fpcxOKQyhUJEhj-PjqJ7Ktj9BRvT_IjN3KJmsqC9bT3vLtjBhPCf2-biWbRL2MbdQRvP_IoG2Mn8M4bb3qOpBtQmJeTxoUJ25DnJhbLGe4bK-TryDa0jqx5',
        }
        for eve_json_data in range(len(json_data_list)):
            try:
                # id
                item['id_acg'] = json_data_list[eve_json_data]['id']
                # category
                item['category'] = json_data_list[eve_json_data]['category']
                # qid
                item['qid'] = json_data_list[eve_json_data]['qid']
                # jumpUrl
                jumpUrl = json_data_list[eve_json_data]['jumpUrl']
                """
                    éčĻå¯šjumpUrlåæå
                """
                pattern_uign = re.compile('uign=(.*?)&')
                uign = re.findall(pattern_uign, jumpUrl)[0]
                pattern_url = re.compile('url=(.*?)&')
                jumpurl_url = re.findall(pattern_url, jumpUrl)[0]
                pattern_category = re.compile('category=(.*?)&')
                category = re.findall(pattern_category, jumpUrl)[0]
                pattern_brand = re.compile('brand=(.*?)&')
                brand = re.findall(pattern_brand, jumpUrl)[0]
                pattern_xzhid = re.compile('xzhid=(.*?)&')
                xzhid = re.findall(pattern_xzhid, jumpUrl)[0]

                # from
                item['from_source'] = json_data_list[eve_json_data]['from']
                # location
                item['location'] = json_data_list[eve_json_data]['location']
                # url
                canshu_url = json_data_list[eve_json_data]['mpObj']['url']
                # įąģåĢ
                item['query'] = json_data_list[eve_json_data]['mpObj']['query']
                # sv_cr
                sv_cr = json_data_list[eve_json_data]['sv_cr']
                if 'nquery' in jumpUrl:
                    url = 'https://b2b.baidu.com/land/viewajax?iid=' + json_data_list[eve_json_data]['id'] + '&query=' + \
                          json_data_list[eve_json_data]['mpObj'][
                              'query'] + '&uign=' + uign + '&url=' + jumpurl_url + '&sv_cr=' + sv_cr + '&timeSignOri=1630035478&miniId=8469&qid=3518344367&is_wise=1&category=' + category + '&brand=' + brand + '&logid=3542512157569618583&xzhid=' + xzhid + '&srcId=27730&ii_pos=' + str(
                        eve_json_data) + '&nquery=' + json_data_list[eve_json_data]['mpObj']['query']
                    yield scrapy.Request(url=url, headers=headers, method='POST', callback=self.parse1,
                                         dont_filter=True, meta={'item': item})
                else:
                    url = 'https://b2b.baidu.com/land/viewajax?iid=' + json_data_list[eve_json_data]['id'] + '&query=' + \
                          json_data_list[eve_json_data]['mpObj'][
                              'query'] + '&uign=' + uign + '&url=' + jumpurl_url + '&sv_cr=' + sv_cr + '&timeSignOri=1630035478&miniId=8469&qid=3518344367&is_wise=1&category=' + category + '&brand=' + brand + '&logid=3542512157569618583&xzhid=' + xzhid + '&srcId=27730&ii_pos=' + str(
                        eve_json_data)
                    yield scrapy.Request(url=url, headers=headers, method='POST', callback=self.parse1,
                                         dont_filter=True, meta={'item': item})
            except:
                pass

    def parse1(self, response):
        item = response.meta['item']
        if response.json()['status'] == 0:
            json_data = response.json()['data']
            # į§įąģ
            item['query_'] = json_data['query']
            # äē§åå
            item['fullname'] = json_data['item']['fullName']
            # įąģåĢ
            item['category_'] = json_data['item']['category']
            # äģˇæ ŧ
            price = json_data['item']['priceList'][0]['price']
            if '.' in price:
                price = price.split('.')[0]

            # č´§å¸åäŊ
            item['priceCurrency'] = json_data['item']['priceList'][0]['priceCurrency']
            if item['priceCurrency'] == "":
                item['price'] = price
            elif item['priceCurrency'] == "ä¸":
                item['price'] = str(int(price) * 10000)
            elif item['priceCurrency'] == "å":
                item['price'] = price
            # č´§įŠčŽĄįŽåäŊ
            unitCode = json_data['item']['priceList'][0]['unitCode']
            if unitCode == 'åå':
                item['unitCode'] = 'kg'
            else:
                item['unitCode'] = unitCode
            # č´§įŠæå°čĩˇæšé
            item['minValue'] = json_data['item']['priceList'][0]['minValue']
            # č´§įŠæå¤§č´­äš°é
            item['maxValue'] = json_data['item']['priceList'][0]['maxValue']
            # čįŗģäēē
            item['contact'] = json_data['btmSellerInfo']['contact']
            # čįŗģäēēįĩč¯
            item['phone'] = json_data['btmSellerInfo']['phone']
            # email
            item['email'] = json_data['btmSellerInfo']['email']
            # čįŗģäēēå§å
            item['contactName'] = json_data['sellerInfo']['contactName']
            # čįŗģäēēåžŽäŋĄåˇ
            item['wechatNumber'] = json_data['sellerInfo']['wechatNumber']
            # å¤é¨å°å
            item['externalAddress'] = json_data['sellerInfo']['externalAddress']
            # å¤é¨å°å2
            item['address_v2'] = json_data['sellerInfo']['address_v2']
            # å°å
            item['address'] = json_data['btmSellerInfo']['address']
            if json_data['btmSellerInfo']['addressV2']:
                # å°åå-åŦå¸
                item['addr'] = json_data['btmSellerInfo']['addressV2']['addr']
                # å°åå-įäģŊ
                item['province'] = json_data['btmSellerInfo']['addressV2']['province']
                # å°åå-åå¸
                item['city'] = json_data['btmSellerInfo']['addressV2']['city']
                # å°åå-å°åē
                item['district'] = json_data['btmSellerInfo']['addressV2']['district']
                # å°åå-čĄé
                item['street'] = json_data['btmSellerInfo']['addressV2']['street']
                # å°åå-
                item['userDetail'] = json_data['btmSellerInfo']['addressV2']['userDetail']
            else:
                # å°åå-åŦå¸
                item['addr'] = ''
                # å°åå-įäģŊ
                item['province'] = ''
                # å°åå-åå¸
                item['city'] = ''
                # å°åå-å°åē
                item['district'] = ''
                # å°åå-čĄé
                item['street'] = ''
                # å°åå-
                item['userDetail'] = ''
            # äžåēå
            item['provider_name'] = json_data['provider']['name']
            # äžåēåįļæ
            item['provider_status'] = json_data['provider']['status']
            # äžåēåæŗ¨åčĩé
            item['provider_regCap'] = json_data['provider']['regCap']
            # äžåēåæŗ¨åå°å
            item['provider_regAddr'] = json_data['provider']['regAddr']
            # äžåēåä¸åĄčå´
            item['provider_scope'] = json_data['provider']['scope']
            # įąäŧæĨä¸č¯ĨåŦå¸äŋĄæ¯éžæĨ
            item['provider_jumpUrl'] = json_data['provider']['jumpUrl']
            # æåĨæļé´
            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
