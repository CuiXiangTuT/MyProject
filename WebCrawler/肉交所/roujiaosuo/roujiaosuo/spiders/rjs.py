import emoji
import scrapy
import re
from datetime import timedelta
import time
from datetime import datetime
from ..items import RoujiaosuoItem
from scrapy.spiders import Spider, Request


class RjsSpider(Spider):
    name = 'rjs'
    # redis_key = 'myspider:start_urls'
    allowed_domains = []

    # start_urls = ['http://www.roujiaosuo.com/mobile/category_api.php?action=getcat&modid=5']

    def start_requests(self):

        sort_url = 'http://www.roujiaosuo.com/mobile/category_api.php?action=getcat&modid=5'
        yield Request(url=sort_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        headers = {
            "User-Agent": "Android/1.76/samsungSM-G977N/7.1.2/cpu:0",
            "Host": "www.roujiaosuo.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
        }
        item = RoujiaosuoItem()

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

                for p in range(1, 201):
                    url = 'http://www.roujiaosuo.com/mobile/sell_new_api.php?action=list&cangku=&chandi=&page=' + str(
                        p) + '&catid=' + \
                          detail_url['catid'] + '&modid=5&token=&vlidate='
                    # print(url)
                    yield Request(url=url, headers=headers, callback=self.parse2, dont_filter=True,
                                  meta={'item': item})
        else:
            print('程序运行结束...')

    def parse2(self, response):
        item = response.meta['item']
        try:
            json_detail_data = response.json()['data']
            for i in range(len(json_detail_data)):
                # 名称
                c = emoji.demojize(json_detail_data[i]['title'])
                emoji_str = emoji.demojize(c)
                item['product_name'] = re.sub(r':(.*?):', '', emoji_str).strip()
                # 产品图片
                item['thumb'] = json_detail_data[i]['thumb']

                itemid = json_detail_data[i]['itemid']
                # 商户名称
                item['company'] = json_detail_data[i]['pubUser']['company']
                # 产品类型
                inner_url = 'http://www.roujiaosuo.com/mobile/sell_api.php'
                data = {
                    'action': 'show',
                    'itemid': itemid,
                    'token': '',
                }
                yield scrapy.FormRequest(url=inner_url, callback=self.parse3, dont_filter=True, formdata=data,
                                         meta={'item': item})
        except:
            pass

    def parse3(self, response):
        item = response.meta['item']
        try:
            # 供应详情页数据
            json_inner_data = response.json()['data']
            # 用户姓名代号
            item['username'] = json_inner_data['userinfo']['username']
            # 业务
            item['business'] = json_inner_data['userinfo']['business']

            # 产品类型
            item['good_sort'] = json_inner_data['result']['zhut']
            # 国家
            item['good_chandi'] = json_inner_data['result']['chandi']
            # 提取厂号

            if re.search(r'\d', item['product_name']) and re.search(r'[A-Za-z]', item['product_name']) and '-' not in \
                    item[
                        'product_name'] and '号' not in item['product_name'] and 'kg' not in item[
                'product_name'] and '级' not in \
                    item['product_name'] and '/' not in item['product_name']:
                pattern = re.compile('[\u4e00-\u9fa5]*([0-9a-zA-Z+])+[\u4e00-\u9fa5]*')
                s = re.search(pattern, item['product_name'])[0]
                item['good_changhao'] = re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039])", "", s)
            elif '-' in item['product_name'] and '号' not in item['product_name'] and 'kg' not in item[
                'product_name'] and '级' not in item['product_name'] and '/' not in item['product_name']:
                h = item['product_name'].split('-')
                p = []
                for z in h:
                    pattern = re.compile('[\u4e00-\u9fa5]*([0-9a-zA-Z+])+[\u4e00-\u9fa5]*')
                    s = re.search(pattern, z)[0]
                    p.append(re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039])", "", s))
                item['good_changhao'] = '-'.join(p)
            elif '/' in item['product_name'] and '号' not in item['product_name'] and 'kg' not in item[
                'product_name'] and '级' not in item['product_name']:
                h = item['product_name'].split('/')
                p = []
                for z in h:
                    pattern = re.compile('[\u4e00-\u9fa5]*([0-9a-zA-Z+])+[\u4e00-\u9fa5]*')
                    s = re.search(pattern, z)[0]
                    p.append(re.sub(u"([^\u0041-\u005a\u0061-\u007a\u0030-\u0039])", "", s))
                item['good_changhao'] = '/'.join(p)

            elif re.sub("\D", '', item['product_name']) and '号' not in item['product_name'] and 'kg' not in item[
                'product_name'] and '级' not in item['product_name']:
                item['good_changhao'] = re.sub("\D", '', item['product_name'])
            elif ''.join(re.findall(r'[A-Za-z]', item['product_name'])) and '号' not in item[
                'product_name'] and 'kg' not in \
                    item['product_name'] and '级' not in item['product_name']:
                item['good_changhao'] = ''.join(re.findall(r'[A-Za-z]', item['product_name']))

            else:
                item['good_changhao'] = '-1'

            if json_inner_data['result']['unit'] == '公斤':
                # 价格
                item['good_price'] = str(float(json_inner_data['result']['price']) * 1000)
                # 数量
                item['good_count'] = str(float(json_inner_data['result']['amount']) / 1000)
            else:

                # 价格
                item['good_price'] = json_inner_data['result']['price']
                # 数量
                item['good_count'] = json_inner_data['result']['amount']

            # 库位
            item['good_cangku'] = json_inner_data['result']['cangku']
            # 联系人姓名
            item['contact_person_name'] = json_inner_data['userinfo']['truename']
            # 联系人头像
            item['contact_person_img'] = json_inner_data['userinfo']['ava_img']
            # 联系人电话
            item['contact_person_phone'] = json_inner_data['userinfo']['mobile']
            # 商户链接
            item['merchant_url'] = 'http://www.roujiaosuo.com/com/' + json_inner_data['userinfo']['username']
            # 更新时间
            t = json_inner_data['result']['edittime']
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
            item['update_time'] = time.strftime("%Y/%m/%d %H:%M", s.timetuple()) if type(s) != str else s
            # 求购
            item['buy_supply'] = '供应'
            # 数据来源
            item['data_source'] = '肉交所'
            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(item)
            yield item
        except:
            pass
