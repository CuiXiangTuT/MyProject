import datetime

import scrapy


class SybgySpider(scrapy.Spider):
    name = 'sybgy'
    allowed_domains = ['cn.toocle.com']

    # start_urls = ['http://www.cn.toocle.com/']
    def start_requests(self):
        item = {}
        for meatName in ['牛肉', '羊肉']:
            for i in range(1, 49):
                url = 'https://cn.toocle.com/search/index.php?f=product&terms={}&p={}.html'.format(meatName, i)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                    # 'Referer': 'https://cn.toocle.com/search/index.php?f=product&terms={}&p={}.html'.format(meatName,i),
                }
                item['meatName'] = meatName
                yield scrapy.Request(url=url, headers=headers, callback=self.parse, dont_filter=True,
                                     meta={'item': item})

    def parse(self, response):
        item = response.meta['item']

        div_list = response.xpath('//div[@class="item-pro-color"]')
        for eve_div in div_list:
            # 产品名
            item['title'] = \
            eve_div.xpath('.//h3[contains(@class,"product-title") and contains(@class,"mb-3")][1]/a/text()')[
                0].extract()
            # 公司
            item['company'] = \
            eve_div.xpath('.//h3[contains(@class,"product-title") and contains(@class,"mb-3")][2]/a/text()')[
                0].extract()
            # 价格
            item['price'] = eve_div.xpath('.//div[@class="product-info"]//div[@class="product-price"]/ins/span/text()')[
                0].extract().strip()
            # 联系方式url
            url = eve_div.xpath('.//h3[contains(@class,"product-title") and contains(@class,"mb-3")][2]/a/@href')[
                      0].extract() + 'company.html'
            # referer
            referer = eve_div.xpath('./div[@class="product-thumb"]/a/@href')[0].extract()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                # 'Referer': '{}'.format(referer),
            }

            yield scrapy.Request(url=url,headers=headers,callback=self.parse1,dont_filter=True,meta={'item':item})

    def parse1(self,response):
        item = response.meta['item']
        try:
            # 联系人
            item['contact'] = response.xpath('//div[contains(@class,"col-9") and contains(@class,"info-section-intro")]/p/text()')[1].extract()
        except:
            item['contact'] = ''
        try:
            # 联系电话
            item['phone'] = response.xpath('.//div[contains(@class,"col-9") and contains(@class,"info-section-intro")]/p/text()')[2].extract()
        except:
            item['phone'] = ''
        try:
            # 手机
            item['mobile'] = response.xpath('.//div[contains(@class,"col-9") and contains(@class,"info-section-intro")]/p/text()')[3].extract()
        except:
            item['mobile'] = ''
        try:
            # 联系传真
            item['fax'] = response.xpath('.//div[contains(@class,"col-9") and contains(@class,"info-section-intro")]/p/text()')[4].extract()
        except:
            item['fax'] = ''
        try:
            # 联系地址
            item['addr'] = response.xpath('.//div[contains(@class,"col-9") and contains(@class,"info-section-intro")]/p/text()')[7].extract()
        except:
            item['addr'] = ''
        try:
            # 邮编
            item['postCodes'] = response.xpath('.//div[contains(@class,"col-9") and contains(@class,"info-section-intro")]/p/text()')[8].extract()
        except:
            item['postCodes'] = ''
        item['cur_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield item
