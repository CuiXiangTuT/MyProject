from datetime import datetime
from ..items import YimutianchandihangqingItem
import scrapy


class YmtcdhqSpider(scrapy.Spider):
    name = 'ymtcdhq'
    allowed_domains = ['hangqing.ymt.com']
    # start_urls = ['http://www.hangqing.ymt.com/']


    def start_requests(self):
        urlList = ['http://hangqing.ymt.com/chandi_489012_0_0/{}', 'http://hangqing.ymt.com/chandi_8173_0_0/{}']
        pageCount = [6, 13]
        zipCount = list(zip(urlList,pageCount))
        item = YimutianchandihangqingItem()
        for perZip in zipCount:
            for pageNum in range(1,perZip[1]):
                if perZip[0]=='http://hangqing.ymt.com/chandi_489012_0_0/{}':
                    # 类别
                    item['meatClass'] = '羊肉'
                else:
                    item['meatClass'] = '牛肉'
                url = perZip[0].format(pageNum)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36'
                }
                yield scrapy.Request(url=url,headers=headers,dont_filter=True,callback=self.parse,meta={'item':item})

    def parse(self, response):
        item = response.meta['item']
        liList = response.xpath('//li[contains(@class,"li_list") and contains(@class,"clearfix")]')
        for everyLi in liList:
            # 地方
            item['address'] = everyLi.xpath('.//div[contains(@class,"c_price_list_addr") and contains(@class,"c_subMainBox")]/p/text()')[0].extract()
            # 品类
            item['meatSort'] = everyLi.xpath('.//span[@class="c_price_cate_name"]/text()')[0].extract()
            # 价格
            item['price'] = everyLi.xpath('.//span[@class="c_price_unit"]/text()')[0].extract()
            # 趋势变化
            item['changeTrend'] = everyLi.xpath('.//span[@class="c_price_cate_unit"]//span[2]/text()')[0].extract()
            # 详情url
            detailUrl = everyLi.xpath('.//div[@class="c_price_user"]//a/@href')[0].extract()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36'
            }
            yield scrapy.Request(url=detailUrl,headers=headers,dont_filter=True,callback=self.parse1,meta={'item':item})


    def parse1(self,response):
        item = response.meta['item']

        # 时间列表
        timeList = response.xpath('//ul[@class="sorts"]//li')
        # 内容列表
        contentList =  response.xpath('//ul[contains(@class,"c_category_list")]')
        zipList = list(zip(timeList,contentList))
        print(len(zipList))
        for everyZip in range(len(zipList)):
            # 时间
            item['Ctime'] = zipList[everyZip][0].xpath('./a/text()')[0].extract()
            liList = zipList[everyZip][1].xpath('.//li')
            for everyLi in range(len(liList)):
                # 品类
                item['detailMeat'] = liList[everyLi].xpath('.//span[@class="c_category_list_li_title"]/text()')[0].extract()
                # 价格
                item['detailPrice'] = liList[everyLi].xpath('.//span[@class="c_category_list_li_unit"]/text()')[0].extract()
                # 趋势变化
                item['detailChangeTrend'] = liList[everyLi].xpath('.//span[contains(@class,"c_category_list_li_status")]/text()')[0].extract()
                # 插入时间
                item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield item





