import datetime

import scrapy
import re
import time
import pytesseract
from PIL import Image
from selenium import webdriver
from ..items import NiurouhuigongyingItem


class NrhgySpider(scrapy.Spider):
    name = 'nrhgy'
    allowed_domains = ['http://nrh.99114.com/']
    start_urls = ['http://http://nrh.99114.com//']

    def start_requests(self):
        for pageNum in range(1, 823):
            url = 'http://nrh.99114.com/supply/l_%E7%89%9B%E8%82%89_0_0_0_0_0_0_0_{}.html'.format(pageNum)
            headers = {
                'Referer': 'http://nrh.99114.com/supply/l_%E7%89%9B%E8%82%89_0_0_0_0_0_0_0_822.html',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
            }
            yield scrapy.Request(url=url, headers=headers, dont_filter=True, callback=self.parse)


    def parse(self, response):
        ulList = response.xpath('//ul[@class="supListUl"]')
        for perUl in ulList:
            # 详情页url
            url = 'http://nrh.99114.com' + perUl.xpath('.//em/a/@href')[0].extract()
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Referer': 'http://nrh.99114.com/supply/l_%E7%89%9B%E8%82%89_0_0_0_0_0_0_0_1.html',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
            }
            yield scrapy.Request(url=url, headers=headers, dont_filter=True, callback=self.parse1)

    def parse1(self, response):
        item = NiurouhuigongyingItem()
        # 种类：牛肉
        item['meatSort'] = '牛肉'
        # 产品名
        item['title'] = \
            response.xpath('//div[contains(@class,"con-title") and contains(@class,"textC")]/h2/span/text()')[
                0].extract().strip()

        try:
            # 订货量
            item['orderQuantity'] = ''.join(
                response.xpath('//tr[@class="tr-first"]/td/text()').extract().split()).replace(u'\u3000', u'')
        except:
            # 订货量
            item['orderQuantity'] = ''

        # ----------------------------------------------------获取价格------------------------------------------------------
        try:
            # 价格
            item['price'] = ''.join(
                response.xpath('//tr[@class="tr-first"]//td[2]/span/text()').extract()).strip().replace(u'\u3000', u'')
        except:
            # 价格
            item['price'] = ''.join(response.xpath(
                '//div[contains(@class,"dp-table") and contains(@class,"dp_proDetail_t")]/table/thead/tr/th/span/text()')[
                                        0].extract()).strip().replace(u'\u3000', u'')
        # -----------------------------------------------------价格单位-----------------------------------------------------
        try:
            # 单位
            item['unit'] = ''.join(response.xpath('//tr[@class="tr-first"]//td[2]/text()').extract()).strip().replace(
                u'\u3000', u'')
        except:
            # 单位
            item['unit'] = ''.join(response.xpath(
                '//div[contains(@class,"dp-table") and contains(@class,"dp_proDetail_t")]/table/thead/tr/th/text()')[
                                       0].extract()).strip().replace(u'\u3000', u'')
        # -----------------------------------------------------市场价-----------------------------------------------------
        try:
            # 市场价
            item['marketPrice'] = ''.join(response.xpath('//span[@id="promotion_price"]/text()').extract()).strip()
        except:
            # 市场价
            item['marketPrice'] = ''.join(
                response.xpath('//div[@class="dp-table2"]/table/tr/td/span/text()').extract()).strip().replace(
                u'\u3000', u'')
        # -----------------------------------------------------市场价单位-----------------------------------------------------
        try:
            # 市场价单位
            item['marketPriceUnit'] = ''.join(
                response.xpath('//div[contains(@class,"dp-table2") and contains(@class,"xunpanT")]/table/tr/td/text()')[
                    1].extract()).strip().replace(u'\u3000', u'')
        except:
            # 市场价单位
            item['marketPriceUnit'] = ''.join(
                response.xpath('//div[@class="dp-table2"]/table//tr[1]/td[1]/text()').extract()).strip().replace(
                u'\u3000', u'')
        # -----------------------------------------------------发货地-----------------------------------------------------
        try:
            # 发货地
            item['placeOfShipment'] = ''.join(response.xpath(
                '//div[contains(@class,"dp-table2") and contains(@class,"xunpanT")]/table//tr[2]//td[2]/span/text()')[
                                                  0].extract()).strip().replace(u'\u3000', u'')
        except:
            item['placeOfShipment'] = ''.join(
                response.xpath('//span[@class="areaname"]/text()')[0].extract()).strip().replace(u'\u3000', u'')
        # -----------------------------------------------------联系人-----------------------------------------------------
        try:
            # 联系人
            item['contact'] = \
                ''.join(response.xpath('//div[@class="contact-p"]/ul//li[1]/text()')[0].extract()).strip().split(':')[1]
        except:
            item['contact'] =''
        # -----------------------------------------------------联系电话-----------------------------------------------------
        # 获取电话
        try:
            # 电话
            item['phone'] = response.xpath('//div[@class="card_des"]//p[2]//span[2]/text()')[0].extract()
        except:
            res = response.body.decode(response.encoding)
            # 获取img的URL
            imgUrlSrcPattern = re.compile('手机:<img src="(.*?)"')
            imgSrc = re.findall(pattern=imgUrlSrcPattern, string=res)[0]
            imgUrl = 'http://niurou.99114.com' + imgSrc
            # 配置无界面浏览器，目的是为了将该图片的url打开并进行截图，因为该url后缀名为.html，为了能够拿到图片，需要对其进行截图
            # 添加参数，不让无界面浏览器打开
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome = webdriver.Chrome(chrome_options=chrome_options)
            chrome.get(imgUrl)
            # 给予一定的反应时间，以让浏览器打开
            time.sleep(2)
            # 全截屏进行截图保存
            chrome.save_screenshot(r'../../imgFile/phone.jpg')
            # 找到img标签所在的位置
            imgPhone = chrome.find_element_by_xpath('//img')
            left = imgPhone.location['x']  # 区块截图左上角在网页中的x坐标
            top = imgPhone.location['y']  # 区块截图左上角在网页中的y坐标
            right = left + imgPhone.size['width']  # 区块截图右下角在网页中的x坐标
            bottom = top + imgPhone.size['height']  # 区块截图右下角在网页中的y坐标
            phone = Image.open(r'../../imgFile/phone.png')
            # 进行区域性截图保存，名字仍为原先的，以覆盖
            phone = phone.crop((left, top, right, bottom))
            phone.save(r'../../imgFile/phone.jpg')
            chrome.quit()
            # 进行识别
            text = pytesseract.image_to_string(Image.open(r'../../imgFile/phone.png'), lang="eng")
            patternPhone = re.compile('(\d){11}')
            phoneStr = re.search(patternPhone, text).group()
            item['phone'] = phoneStr
        # -----------------------------------------------------邮箱-----------------------------------------------------
        # 获取邮箱
        try:
            # 邮箱
            item['email'] = response.xpath('//div[@class="card_des"]//p[3]//span[2]/text()')[0].extract()
        except:
            # 获取img的URL
            res = response.body.decode(response.encoding)
            # 获取img的URL
            imgUrlSrcPattern = re.compile('邮箱:<img src="(.*?)"')
            imgSrc = re.findall(pattern=imgUrlSrcPattern, string=res)[0]
            imgUrl = 'http://niurou.99114.com' + imgSrc
            print(imgUrl)
            # 配置无界面浏览器，目的是为了将该图片的url打开并进行截图，因为该url后缀名为.html，为了能够拿到图片，需要对其进行截图
            # 添加参数，不让无界面浏览器打开
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome = webdriver.Chrome(chrome_options=chrome_options)
            chrome.get(imgUrl)
            # 给予一定的反应时间，以让浏览器打开
            time.sleep(2)
            # 全截屏进行截图保存
            chrome.save_screenshot(r'../../imgFile/email.png')
            # 找到img标签所在的位置
            imgPhone = chrome.find_element_by_xpath('//img')
            left = imgPhone.location['x']  # 区块截图左上角在网页中的x坐标
            top = imgPhone.location['y']  # 区块截图左上角在网页中的y坐标
            right = left + imgPhone.size['width']  # 区块截图右下角在网页中的x坐标
            bottom = top + imgPhone.size['height']  # 区块截图右下角在网页中的y坐标
            phone = Image.open(r'../../imgFile/email.png')
            # 进行区域性截图保存，名字仍为原先的，以覆盖
            phone = phone.crop((left, top, right, bottom))
            phone.save(r'../../imgFile/email.png')
            chrome.quit()
            # 进行识别
            text = pytesseract.image_to_string(Image.open(r'../../imgFile/email.png'), lang="eng")
            patternPhone = re.compile('[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\. [com,cn,net]{1,3}')
            phoneStr = re.findall(patternPhone, text)[0]
            item['email'] = phoneStr
        item['curTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield item
