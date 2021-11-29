import datetime

import scrapy
from ..items import YangxianmenggongyingItem


class YxmgySpider(scrapy.Spider):
    name = 'yxmgy'
    allowed_domains = ['www.yxmon.com']

    # start_urls = ['http://http://www.yxmon.com//']

    def start_requests(self):
        item = YangxianmenggongyingItem()
        meat_sort = ["牛肉", "羊肉"]
        page_sort = [51, 27]
        zip_list = list(zip(meat_sort, page_sort))
        for per_meat in zip_list:
            for i in range(1, per_meat[1]):
                url = 'http://www.yxmon.com/shop/search-index-keyword-{}-curpage-{}.html'.format(per_meat[0], i)
                headers = {
                    'Referer': 'http://www.yxmon.com/shop/search-index-keyword-{}-curpage-1.html?act=search&op=index&keyword={}'.format(
                        per_meat[0], per_meat[0]),
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                }
                item['meat_name'] = per_meat[0]
                yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True,
                                     meta={"item": item})

    def parse(self, response):
        tr_list = response.xpath('//div[@class="c_item_table"]/table//tr')
        item = response.meta['item']
        for eve_tr in tr_list:
            # 产品url
            url = eve_tr.xpath('.//td[contains(@class,"c_left") and contains(@class,"c_goods_name")]/a/@href')[
                0].extract()
            headers = {

                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'no-cache',
                'Cookie': 'PHPSESSID=4ipr58f4lip53ekqa26ai4n5q2; 1F10_cart_goods_num=0; Hm_lvt_7825a541ebf6a4de7851e84c0320f5cb=1629767744,1629939558,1630132186; Hm_lpvt_7825a541ebf6a4de7851e84c0320f5cb=1630133480',
                'Host': 'www.yxmon.com',
                'Pragma': 'no-cache',
                # 'Proxy-Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',

                # 'Referer': 'http://www.yxmon.com/shop/search-index-keyword-{}-curpage-1.html'.format(item['meat_name']),
                # 'Upgrade-Insecure-Requests': '1',
                # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                # 'Cookie': 'PHPSESSID=4ipr58f4lip53ekqa26ai4n5q2; 1F10_cart_goods_num=0; Hm_lvt_7825a541ebf6a4de7851e84c0320f5cb=1629767744,1629939558,1630132186; Hm_lpvt_7825a541ebf6a4de7851e84c0320f5cb=1630133533'
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.parse1, dont_filter=True, meta={"item": item})

    def parse1(self, response):
        item = response.meta['item']
        # 产品名
        item['title'] = response.xpath('//div[contains(@class,"c_2") and contains(@class,"c_goods_exp")]/h1/text()')[
            0].extract().strip()
        if response.xpath('//div[contains(@class,"c_2") and contains(@class,"c_goods_exp")]/h1/div'):
            # 备注信息
            item['remarks'] = \
                response.xpath('//div[contains(@class,"c_2") and contains(@class,"c_goods_exp")]/h1/div/text()')[
                    0].extract()
        else:
            item['remarks'] = '无'
        # 价格梯度
        price_grade = response.xpath('//div[contains(@class,"c_2") and contains(@class,"c_goods_exp")]/dl//dd')
        for eve_grade_index in range(len(price_grade)):
            item['price_' + str(eve_grade_index)] = price_grade[eve_grade_index].xpath('./p/text()')[
                0].extract().replace('￥', '')
            item['priceGrade_' + str(eve_grade_index)] = price_grade[eve_grade_index].xpath('.//p[2]/text()')[
                0].extract()
        # 编号
        ll_list = response.xpath('//div[contains(@class,"padding_20") and contains(@class,"font_size_18")]//ul//li')
        for eve_li in range(len(ll_list)):
            eve_li_data = ll_list[eve_li].xpath('./text()')[0].extract().strip()
            if '编号' in eve_li_data:
                item['No'] = eve_li_data.split('：')[1]

            if '品牌' in eve_li_data:
                item['brand'] = eve_li_data.split('：')[1]

            if '厂号' in eve_li_data:
                item['factoryNo'] = eve_li_data.split('：')[1].replace('厂', '')

            if '生产日期' in eve_li_data:
                item['dateOfManufacture'] = eve_li_data.split('：')[1]

            if '产地' in eve_li_data:
                item['placeOfOrigin'] = eve_li_data.split('：')[1]

            if '保质期' in eve_li_data:
                item['qualityGuaranteePeriod'] = eve_li_data.split('：')[1]

            if '等级' in eve_li_data:
                item['goodsGrade'] = eve_li_data.split('：')[1]

        # 店铺名称
        item['storeName'] = \
            response.xpath('//div[contains(@class,"c_3") and contains(@class,"c_shop_info")]/h3/a/text()')[0].extract()
        # 店铺电话
        text_list = response.xpath('//div[contains(@class,"c_3") and contains(@class,"c_shop_info")]//ul//li')
        for eve_sel in text_list:
            eve_sel = eve_sel.xpath('./text()')[0].extract().strip()
            if '店铺电话' in eve_sel:
                item['store_phone'] = eve_sel.split('：')[1]

            if '地域信息' in eve_sel:
                item['location'] = eve_sel.split('：')[1]
        # 遍历item字典，将缺失的键值做填充，以便后续数据入库
        if 'No' not in item.keys():
            item['No'] = ''
        if 'brand' not in item.keys():
            item['brand'] = ''
        if 'factoryNo' not in item.keys():
            item['factoryNo'] = ''
        if 'dateOfManufacture' not in item.keys():
            item['dateOfManufacture'] = ''
        if 'placeOfOrigin' not in item.keys():
            item['placeOfOrigin'] = ''
        if 'qualityGuaranteePeriod' not in item.keys():
            item['qualityGuaranteePeriod'] = ''
        if 'goodsGrade' not in item.keys():
            item['goodsGrade'] = ''
        if 'price_0' not in item.keys():
            item['price_0'] = ''
        if 'price_1' not in item.keys():
            item['price_1'] = ''
        if 'price_2' not in item.keys():
            item['price_2'] = ''
        if 'price_3' not in item.keys():
            item['price_3'] = ''
        if 'priceGrade_0' not in item.keys():
            item['priceGrade_0'] = ''
        if 'priceGrade_1' not in item.keys():
            item['priceGrade_1'] = ''
        if 'priceGrade_2' not in item.keys():
            item['priceGrade_2'] = ''
        if 'priceGrade_3' not in item.keys():
            item['priceGrade_3'] = ''
        item['cur_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield item
