from pprint import pprint
import scrapy
import re
from datetime import timedelta
import time
from datetime import datetime
from ..items import RoujiaosuocaigouItem
from scrapy.spiders import Spider, Request


class RjscgSpider(scrapy.Spider):
    name = 'rjscg'
    allowed_domains = ['www.roujiaosuo.com']
    start_urls = ['http://www.roujiaosuo.com/']
    allowed_domains = ['www.roujiaosuo.com']

    # start_urls = ['http://www.roujiaosuo.com/']
    # allowed_domains = ['http://www.roujiaosuo.com']

    def start_requests(self):
        url = 'http://www.roujiaosuo.com/mobile/category_api.php?action=getcat&modid=6'
        yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        headers = {
            "User-Agent": "Android/1.76/samsungSM-G977N/7.1.2/cpu:0",
            "Host": "www.roujiaosuo.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        item = RoujiaosuocaigouItem()
        # 采购
        item['buy_supply'] = '采购'
        # 来源
        item['data_source'] = "肉交所"

        # 获取牛产品和羊产品的相关列表数据
        json_data = response.json()['data']['far_catid']

        # 定义一个空列表，用来只存放牛羊肉
        use_meat = [json_data[1], json_data[2]]

        for c in use_meat:
            # 一级类别
            item['meat_name'] = c['catname']
            # 获取二级标题列表
            detail_meat_list = c['sub'][1:]

            for detail_url in detail_meat_list:
                # 二级类别标题
                item['sec_catname'] = detail_url['catname']
                p = 1
                for p in range(1,201):
                    url = 'http://www.roujiaosuo.com/mobile/buy_api.php?action=list&cangku=&chandi=&page=' + str(
                        p) + '&zhut=&catid=' + detail_url['catid'] + '&modid=6&token='
                    yield Request(url=url, headers=headers, callback=self.parse1, dont_filter=True,
                                  meta={'item': item})



    def parse1(self, response):
        item = response.meta['item']
        json_detail_data = response.json()['data']
        try:
            for i in range(len(json_detail_data)):
                # 名称
                item['product_name'] = json_detail_data[i]['title']
                # 采购要求
                item['buy_requirements'] = json_detail_data[i]['xxyq']
                # 发布时间
                t = json_detail_data[i]['edittime']
                delta = int(re.findall("\d+", t)[0])  # 从obj字符串中中取出相应的数字
                # print(delta,datetime.datetime.now())
                if '秒' in t:  # 如果obj是有秒
                    # print(datetime.timedelta(seconds=delta))
                    s = datetime.now() - timedelta(seconds=delta)
                elif '分钟' in t:  # 如果obj是有分钟
                    s = datetime.now() - timedelta(minutes=delta)
                elif '小时' in t:  # 如果obj是有小时
                    s = datetime.now() - timedelta(hours=delta)
                elif '天' in t:  # 如果obj是有天
                    # print(datetime.timedelta(days=delta))
                    s = datetime.now() - timedelta(days=delta)
                else:  # 如果obj是正常日期
                    s = t
                # print(type(s)==str)
                # 如果type(s)不是str，则返回time.strftime("%Y/%m/%d %H:%M", s.timetuple())；否则，直接返回s
                item['edittime'] = time.strftime("%Y/%m/%d %H:%M", s.timetuple()) if type(s) != str else s

                itemid = json_detail_data[i]['itemid']
                # 产品类型
                inner_url = 'http://www.roujiaosuo.com/mobile/buy_api.php'
                data = {
                    'action': 'show',
                    'itemid': itemid,
                    'token': '',
                }

                yield scrapy.FormRequest(url=inner_url, formdata=data, dont_filter=True, callback=self.parse2,
                                         meta={'item': item})
        except:
            pass

    def parse2(self, response):
        item = response.meta['item']
        # 供应详情页数据
        json_inner_data = response.json()['data']
        try:
            # username
            item['username'] = json_inner_data['userinfo']['username']

            # 姓名
            item['truename'] = json_inner_data['userinfo']['truename']
            # 电话
            item['iphone'] = json_inner_data['userinfo']['mobile']
            if json_inner_data['result']['unit'] == "公斤":
                # 价格
                item['intention_price'] = str(float(json_inner_data['result']['price']) * 1000)
                # 数量
                item['intention_count'] = str(float(json_inner_data['result']['amount']) / 1000)
            else:
                # 意向价格
                item['intention_price'] = json_inner_data['result']['price']
                # 采购数量
                item['intention_count'] = json_inner_data['result']['amount']
            # 产地要求
            item['origin_requirements'] = json_inner_data['result']['chandi']
            # 所在地区-省份 province
            p_location = json_inner_data['result']['mypostion']

            if '/' in p_location:
                item['province'] = p_location.split('/')[0]
                item['city'] = p_location.split('/')[1]
            else:
                item['province'] = p_location
                item['city'] = ''

            # 所在地区-城市 city
            # 状态要求
            item['status_requirements'] = json_inner_data['result']['zhut2']
            # 已采购信息
            item['pubbuy'] = "采购信息" + json_inner_data['userinfo']['pubbuy'] + '条'
            # 有X人联系Ta
            item['telcount'] = "已有" + json_inner_data['userinfo']['telcount'] + "人联系Ta"
            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            pprint(item)
            yield item
        except:
            pass
