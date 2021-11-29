import copy

import emoji
import pymysql
import redis
import scrapy
from datetime import datetime
import json, re
from ..items import BeefuItem
import pandas as pd
import jieba
# from scrapy_redis.spiders import Spider


class BfSpider(scrapy.Spider):
    name = 'bf'

    # allowed_domains = ['GetBeefCircle']

    def start_requests(self):
        for i in range(1, 1000):
            start_urls = 'http://47.96.113.183:8080/api/SystemApi/GetBeefCircle'
            data = {
                "MessageType": 60002,
                "MessageID": "729c8127-ed38-4a2b-9135-3b993241876e",
                "Data": {
                    "PageNum": i,
                    "PageSize": 10,
                    "KeyWords": "",
                    "ContentType": 0
                }
            }
            headers = {
                "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.0)",
                "Content-Type": "application/json; charset=utf-8",
                # "Content-Length": "137",
                "Host": "47.96.113.183:8080",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
            }
            cities = self.read_mysql_city()
            countries = self.read_mysql_country()
            provinces = self.read_mysql_province()
            t_product = self.read_mysql_product1()
            products = self.read_mysql_product()
            additional_area = ['澳洲']
            area_l = countries + provinces + cities + additional_area
            yield scrapy.Request(url=start_urls, headers=headers, callback=self.parse, dont_filter=True,
                                 body=json.dumps(data), method='POST',
                                 meta={'area_l': area_l, 't_product': t_product, 'products': products})

    def parse(self, response):

        al = response.meta['area_l']
        t_product = response.meta['t_product']
        products = response.meta['products']

        json_data = response.json()['Data']['Rows']

        item = BeefuItem()
        pattern = re.compile('(?<!\d)(1\d{10})(?!\d)')
        for i in range(len(json_data)):
            if json_data[i]['UserName'].split('-'):
                # 公司+姓名
                username = json_data[i]['UserName'].split('-')
                if len(username) == 2:
                    # 蒙之羊-13592575735
                    if re.findall(pattern, username[1]):
                        item['company'] = username[0]
                        item['phone'] = username[1]
                        c = emoji.demojize(json_data[i]['Content'])
                        emoji_str = emoji.demojize(c)
                        item['content'] = re.sub(r':(.*?):', '', emoji_str).strip()
                        item['contact_person_name'] = ''
                    else:
                        # 'UserName': '上海幽通国际贸易有限公司-陈志新'
                        item['contact_person_name'] = username[1]
                        item['company'] = username[0]
                        # content
                        c = emoji.demojize(json_data[i]['Content'])
                        emoji_str = emoji.demojize(c)
                        item['content'] = re.sub(r':(.*?):', '', emoji_str).strip()
                        emoji_str = emoji.demojize(item['content'])
                        k = re.sub(r':(.*?):', '', emoji_str).strip()
                        v = re.findall(pattern, k)
                        if len(v):
                            item['phone'] = v[0]
                        else:
                            item['phone'] = ''


                elif len(username) == 3:
                    # 上海希牛贸易有限公司-15666969979-王玉静
                    item['company'] = username[0]
                    item['phone'] = username[1]
                    item['contact_person_name'] = username[2]
                    # item['content'] = str(
                    #     bytes(json_data[i]['Content'], encoding='utf-8').decode('utf-8').encode('gbk', 'ignore').decode(
                    #         'gbk'))
                    c = emoji.demojize(json_data[i]['Content'])
                    emoji_str = emoji.demojize(c)
                    item['content'] = re.sub(r':(.*?):', '', emoji_str).strip()

            content1 = re.sub(item['phone'], '', item['content'])
            item['new_content'] = re.sub(item['company'], '', content1)
            if '求购' in item['new_content']:
                item['buy_supply'] = '求购'
                # 储存地名的下标
                al_index = []
                # 储存地名
                al_add = []
                for c in al:
                    for i in range(len(item['new_content']) - 1):
                        if item['new_content'][i:i + 4] == c:
                            al_index.append((i, i + 4))
                            al_add.append(item['new_content'][i:i + 4])
                        if item['new_content'][i:i + 3] == c:
                            al_index.append((i, i + 3))
                            al_add.append(item['new_content'][i:i + 3])
                        if item['new_content'][i:i + 2] == c:
                            al_index.append((i, i + 2))
                            al_add.append(item['new_content'][i:i + 2])
                if len(al_index) == 0 and len(al_add) == 0:
                    item['location'] = ''
                else:
                    # 绑定拿到的地名与存储的地名下标
                    zip_add = list(zip(al_index, al_add))
                    # 用来存放单条信息内容：地名1：信息1，地名2：信息2，地名3：信息3...
                    a_l = sorted(map(sorted, al_index))

                    if len(a_l) == 1:
                        eve_mesg = item['new_content'][:]
                        item = self.get_mesg(eve_mesg, item, products, t_product)
                        return item
                    else:
                        for k in range(len(a_l)):
                            # 情况0：某条数据类似：天津，河北天环两个冷库，全部现货可出，后续数据均为天津河北的
                            #        那么就需要考虑将河北后面的数据添加到天津后面
                            if k + 2 <= len(a_l) and a_l[k][0] - a_l[k - 1][0] == 3:
                                if k + 2 == len(a_l):
                                    eve_mesg = item['new_content'][a_l[k + 1][0]:]
                                    item = self.get_mesg(eve_mesg, item, products, t_product)
                                    return item
                                else:
                                    eve_mesg = item['new_content'][a_l[k + 1][0]:a_l[k + 2][1]]
                                    item = self.get_mesg(eve_mesg, item, products, t_product)
                                    return item

                            # 情况1：存放地址下标的首个元素的初始下标（即a_l[0][0]）不为0，此时需要将前面的内容与到下一个地址前的内容进行拼接
                            if k == 0 and a_l[0][0] != 0 and len(a_l) > 1:
                                eve_mesg = item['new_content'][:a_l[0][0]] + item['new_content'][a_l[0][0]:a_l[1][0]]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[0][0]:a_l[0][1]]
                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
                            # 情况2：抽取除开始和结尾中间的数据，并以地址做切割
                            if k + 1 < len(a_l) and k != 0:
                                # 将信息拿下来了
                                eve_mesg = item['new_content'][a_l[k][0]:a_l[k + 1][0]]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[k][0]:a_l[k][1]]

                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
                            # 情况3：取最后一个数据
                            if k + 1 == len(a_l):
                                eve_mesg = item['new_content'][a_l[-1][0]:]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[-1][0]:a_l[-1][1]]

                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
            if '现货' in item['new_content'] or '采购' in item['new_content'] or '财富' in item['new_content'] or '报盘' in \
                    item['new_content']:
                item['buy_supply'] = '供应'
                # 储存地名的下标
                al_index = []
                # 储存地名
                al_add = []
                for c in al:
                    for i in range(len(item['new_content']) - 1):
                        if item['new_content'][i:i + 4] == c:
                            al_index.append((i, i + 4))
                            al_add.append(item['new_content'][i:i + 4])
                        if item['new_content'][i:i + 3] == c:
                            al_index.append((i, i + 3))
                            al_add.append(item['new_content'][i:i + 3])
                        if item['new_content'][i:i + 2] == c:
                            al_index.append((i, i + 2))
                            al_add.append(item['new_content'][i:i + 2])
                if len(al_index) == 0 and len(al_add) == 0:
                    item['location'] = ''
                else:
                    # 绑定拿到的地名与存储的地名下标
                    zip_add = list(zip(al_index, al_add))
                    # 用来存放单条信息内容：地名1：信息1，地名2：信息2，地名3：信息3...
                    a_l = sorted(map(sorted, al_index))

                    if len(a_l) == 1:
                        eve_mesg = item['new_content'][:]
                        item = self.get_mesg(eve_mesg, item, products, t_product)
                        return item
                    else:
                        for k in range(len(a_l)):
                            # 情况0：某条数据类似：天津，河北天环两个冷库，全部现货可出，后续数据均为天津河北的
                            #        那么就需要考虑将河北后面的数据添加到天津后面
                            if k + 2 <= len(a_l) and a_l[k][0] - a_l[k - 1][0] == 3:
                                if k + 2 == len(a_l):
                                    eve_mesg = item['new_content'][a_l[k + 1][0]:]
                                    item = self.get_mesg(eve_mesg, item, products, t_product)
                                    return item
                                else:
                                    eve_mesg = item['new_content'][a_l[k + 1][0]:a_l[k + 2][1]]
                                    item = self.get_mesg(eve_mesg, item, products, t_product)
                                    return item

                            # 情况1：存放地址下标的首个元素的初始下标（即a_l[0][0]）不为0，此时需要将前面的内容与到下一个地址前的内容进行拼接
                            if k == 0 and a_l[0][0] != 0 and len(a_l) > 1:
                                eve_mesg = item['new_content'][:a_l[0][0]] + item['new_content'][a_l[0][0]:a_l[1][0]]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[0][0]:a_l[0][1]]
                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
                            # 情况2：抽取除开始和结尾中间的数据，并以地址做切割
                            if k + 1 < len(a_l) and k != 0:
                                # 将信息拿下来了
                                eve_mesg = item['new_content'][a_l[k][0]:a_l[k + 1][0]]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[k][0]:a_l[k][1]]

                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
                            # 情况3：取最后一个数据
                            if k + 1 == len(a_l):
                                eve_mesg = item['new_content'][a_l[-1][0]:]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[-1][0]:a_l[-1][1]]

                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
            else:
                item['buy_supply'] = '供应'

                # 储存地名的下标
                al_index = []
                # 储存地名
                al_add = []
                for c in al:
                    for i in range(len(item['new_content']) - 1):
                        if item['new_content'][i:i + 4] == c:
                            al_index.append((i, i + 4))
                            al_add.append(item['new_content'][i:i + 4])
                        if item['new_content'][i:i + 3] == c:
                            al_index.append((i, i + 3))
                            al_add.append(item['new_content'][i:i + 3])
                        if item['new_content'][i:i + 2] == c:
                            al_index.append((i, i + 2))
                            al_add.append(item['new_content'][i:i + 2])
                if len(al_index) == 0 and len(al_add) == 0:
                    item['location'] = ''
                else:
                    # 绑定拿到的地名与存储的地名下标
                    zip_add = list(zip(al_index, al_add))
                    # 用来存放单条信息内容：地名1：信息1，地名2：信息2，地名3：信息3...
                    a_l = sorted(map(sorted, al_index))

                    if len(a_l) == 1:
                        eve_mesg = item['new_content'][:]
                        item = self.get_mesg(eve_mesg, item, products, t_product)
                        return item
                    else:
                        for k in range(len(a_l)):
                            # 情况0：某条数据类似：天津，河北天环两个冷库，全部现货可出，后续数据均为天津河北的
                            #        那么就需要考虑将河北后面的数据添加到天津后面
                            if k + 2 <= len(a_l) and a_l[k][0] - a_l[k - 1][0] == 3:
                                if k + 2 == len(a_l):
                                    eve_mesg = item['new_content'][a_l[k + 1][0]:]
                                    item = self.get_mesg(eve_mesg, item, products, t_product)
                                    return item
                                else:
                                    eve_mesg = item['new_content'][a_l[k + 1][0]:a_l[k + 2][1]]
                                    item = self.get_mesg(eve_mesg, item, products, t_product)
                                    return item

                            # 情况1：存放地址下标的首个元素的初始下标（即a_l[0][0]）不为0，此时需要将前面的内容与到下一个地址前的内容进行拼接
                            if k == 0 and a_l[0][0] != 0 and len(a_l) > 1:
                                eve_mesg = item['new_content'][:a_l[0][0]] + item['new_content'][a_l[0][0]:a_l[1][0]]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[0][0]:a_l[0][1]]
                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
                            # 情况2：抽取除开始和结尾中间的数据，并以地址做切割
                            if k + 1 < len(a_l) and k != 0:
                                # 将信息拿下来了
                                eve_mesg = item['new_content'][a_l[k][0]:a_l[k + 1][0]]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[k][0]:a_l[k][1]]

                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item
                            # 情况3：取最后一个数据
                            if k + 1 == len(a_l):
                                eve_mesg = item['new_content'][a_l[-1][0]:]
                                # 可以将地址率先提取出来
                                item['location'] = item['new_content'][a_l[-1][0]:a_l[-1][1]]

                                item = self.get_mesg(eve_mesg, item, products, t_product)
                                return item

    @staticmethod
    def get_mesg(eve_mesg, item, products, t_product):
        # 现在拿到的已经是单条的信息了

        s = eve_mesg.replace('\n', '，').replace(item['phone'], '').replace('／', ',')

        if '吨' in s:
            pattern_ton = re.compile('(\d){1,4}吨')
            s = re.sub(pattern_ton, '', s)
        if '月' in s:
            pattern_ton = re.compile('(\d){1,2}月')
            s = re.sub(pattern_ton, '', s)
        if 'cl' in s:
            pattern_ton = re.compile('(\d){1,4}cl')
            s = re.sub(pattern_ton, '', s)
        if '号' in s:
            pattern_ton = re.compile('(\d){1,2}.{1}(\d){1,2}号')
            s = re.sub(pattern_ton, '', s)
        s1 = s
        word_list = jieba.lcut(s1, cut_all=False, HMM=True)
        area_list = ['中国', '德国', '丹麦', '西班牙', '荷兰', '英国', '美国', '法国', '爱尔兰', '新西兰', '智利', '阿根廷', '乌拉圭', '加拿大', '澳大利亚',
                     '巴西', '墨西哥', '印度', '缅甸', '巴基斯坦', '印尼', '马来西亚', '西非', '乌克兰', '俄罗斯', '哈萨克斯坦', '比利时', '挪威', '菲律宾',
                     '苏格兰', '法罗群岛', '冰岛', '韩国', '日本', '孟加拉', '厄瓜多尔', '越南', '塞尔维亚', '哥斯达黎加', '南非', '罗马尼亚', '蒙古', '朝鲜',
                     '芬兰', '泰国', '白俄罗斯', '波兰', '土耳其', '索马里', '匈牙利', '纳米比亚', '葡萄牙', '瑞士', '意大利', '拉脱维亚', '巴拿马', '玻利维亚',
                     '奥地利', '立陶宛', '北京', '天津', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省', '黑龙江省', '上海', '江苏省', '浙江省', '安徽省',
                     '福建省', '江西省', '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省', '重庆', '四川省', '贵州省', '云南省',
                     '西藏自治区', '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '台湾', '香港特别行政区', '澳门特别行政区', '北京市', '天津市',
                     '石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市', '衡水市', '太原市', '大同市',
                     '阳泉市', '长治市', '晋城市', '朔州市', '晋中市', '运城市', '忻州市', '临汾市', '吕梁市', '呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市',
                     '鄂尔多斯市', '呼伦贝尔市', '巴彦淖尔市', '乌兰察布市', '兴安盟', '锡林郭勒盟', '阿拉善盟', '沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市',
                     '丹东市', '锦州市', '营口市', '阜新市', '辽阳市', '盘锦市', '铁岭市', '朝阳市', '葫芦岛市', '长春市', '吉林市', '四平市', '辽源市', '通化市',
                     '白山市', '松原市', '白城市', '延边朝鲜族自治州', '哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市', '伊春市', '佳木斯市',
                     '七台河市', '牡丹江市', '黑河市', '绥化市', '大兴安岭地区', '上海市', '南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市',
                     '淮安市', '盐城市', '扬州市', '镇江市', '泰州市', '宿迁市', '杭州市', '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市', '金华市', '衢州市',
                     '舟山市', '台州市', '丽水市', '合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市', '安庆市', '黄山市', '滁州市', '阜阳市',
                     '宿州市', '六安市', '亳州市', '池州市', '宣城市', '福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市', '龙岩市', '宁德市',
                     '南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '吉安市', '宜春市', '抚州市', '上饶市', '济南市', '青岛市', '淄博市',
                     '枣庄市', '东营市', '烟台市', '潍坊市', '济宁市', '泰安市', '威海市', '日照市', '莱芜市', '临沂市', '德州市', '聊城市', '滨州市', '菏泽市',
                     '郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '济源市', '濮阳市', '许昌市', '漯河市', '三门峡市', '南阳市',
                     '商丘市', '信阳市', '周口市', '驻马店市', '武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市', '荆门市', '孝感市', '荆州市', '黄冈市',
                     '咸宁市', '随州市', '恩施土家族苗族自治州', '仙桃市', '潜江市', '天门市', '神农架林区', '长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市',
                     '常德市', '张家界市', '益阳市', '郴州市', '永州市', '怀化市', '娄底市', '湘西土家族苗族自治州', '广州市', '韶关市', '深圳市', '珠海市', '汕头市',
                     '佛山市', '江门市', '湛江市', '茂名市', '肇庆市', '惠州市', '梅州市', '汕尾市', '河源市', '阳江市', '清远市', '东莞市', '中山市', '东沙群岛',
                     '潮州市', '揭阳市', '云浮市', '南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '百色市', '贺州市',
                     '河池市', '来宾市', '崇左市', '海口市', '三亚市', '三沙市', '五指山市', '琼海市', '儋州市', '文昌市', '万宁市', '东方市', '定安县', '屯昌县',
                     '澄迈县', '临高县', '白沙黎族自治县', '昌江黎族自治县', '乐东黎族自治县', '陵水黎族自治县', '保亭黎族苗族自治县', '琼中黎族苗族自治县', '重庆市', '成都市',
                     '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市', '内江市', '乐山市', '南充市', '眉山市', '宜宾市', '广安市', '达州市',
                     '雅安市', '巴中市', '资阳市', '阿坝藏族羌族自治州', '甘孜藏族自治州', '凉山彝族自治州', '贵阳市', '六盘水市', '遵义市', '安顺市', '铜仁市',
                     '黔西南布依族苗族自治州', '毕节市', '黔东南苗族侗族自治州', '黔南布依族苗族自治州', '昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市',
                     '临沧市', '楚雄彝族自治州', '红河哈尼族彝族自治州', '文山壮族苗族自治州', '西双版纳傣族自治州', '大理白族自治州', '德宏傣族景颇族自治州', '怒江傈僳族自治州',
                     '迪庆藏族自治州', '拉萨市', '昌都地区', '山南地区', '日喀则地区', '那曲地区', '阿里地区', '林芝地区', '西安市', '铜川市', '宝鸡市', '咸阳市',
                     '渭南市', '延安市', '汉中市', '榆林市', '安康市', '商洛市', '兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '武威市', '张掖市', '平凉市',
                     '酒泉市', '庆阳市', '定西市', '陇南市', '临夏回族自治州', '甘南藏族自治州', '西宁市', '海东市', '海北藏族自治州', '黄南藏族自治州', '海南藏族自治州',
                     '果洛藏族自治州', '玉树藏族自治州', '海西蒙古族藏族自治州', '银川市', '石嘴山市', '吴忠市', '固原市', '中卫市', '乌鲁木齐市', '克拉玛依市', '吐鲁番地区',
                     '哈密地区', '昌吉回族自治州', '博尔塔拉蒙古自治州', '巴音郭楞蒙古自治州', '阿克苏地区', '克孜勒苏柯尔克孜自治州', '喀什地区', '和田地区', '伊犁哈萨克自治州',
                     '塔城地区', '阿勒泰地区', '石河子市', '阿拉尔市', '图木舒克市', '五家渠市', '台北市', '高雄市', '台南市', '台中市', '金门县', '南投县', '基隆市',
                     '新竹市', '嘉义市', '新北市', '宜兰县', '新竹县', '桃园县', '苗栗县', '彰化县', '嘉义县', '云林县', '屏东县', '台东县', '花莲县', '澎湖县',
                     '连江县', '香港岛', '九龙', '新界', '澳门半岛', '离岛', '澳洲']
        rubbish_word = ['一手', '货源', '整出', '销售', '百夫', '沃德', '最新', '必孚', '可视', '大陆', '进口', '数据', '视图', '点击', '下方', '产品',
                        '销售', '长图', '查看', '产品', '拼柜', '两个', '安采', '大罗', '塘大贸', '即将', '清关', '整柜', '最近', '天气', '凉爽', '正好',
                        '值得', '台风', '工厂', '赶上', '备货', '旺季', '投资', '正在', '比例', '便宜', '而且', '加工', '售卖', '精选', '油少', '容易',
                        '适合', '加工', '先到', '一柜', '先得', '价格', '美丽', '畅销货', '餐饮', '版型', '价格', '名细', '如下', '核酸', '检测', '消毒',
                        '证明', '等级', '可提', '品质', '今日', '头条', '厂西', '财富', '热线', '关中', '柜出', '厂带', '脐橙', '国产', '合适', '微信',
                        '同号', '有限公司', '打扰', '件套', '手机', '安格斯', '群发', '消息', '多有', '极佳', '金钱', '饲全', '性价比', '精修', '七月',
                        '底到', '精品', '几吨', '信号', '五证', '齐全', '厂后', '电话', '编号', '初到', '接受', '订阅', '盐田港', '需要', '短期', '仅剩',
                        '前后', '联系', '要求', '四证', '港口', '天津港', '涨价', '抓紧', '日期', '抢购', '左右', '系列', '侧边', '全厂', '带侧', '少量',
                        '汇洋', '可散', '市场', '最低价', '下周', '货来', '柒号', '采购', '南美', '定金', '留货', '康达明', '清库', '天亿', '昆山',
                        '询价', '上海港', '链条', '统出', '可吨', '正关', '同步', '刘洋', '级佳', '打包', '长期', '四分', '豪之安', '商贸', '手续',
                        '直提', '供应', '拆柜', '翼板', '入库', '刀片', '检疫', '三件套', '白俄', '微电同', '手慢', '薄裙', '以上', '联系电话', '库存',
                        '随时', '提货', '旧货', '不高', '汇昌隆', '随提', '最好', '猪头', '其他', '代友', '厂草', '能带', '公斤', '肥版', '酮体', '大小',
                        '西南郊', '厂前', '阿兰', '双层', '型号', '大包', '花箱', '剩余', '单品', '星期', '下单', '联系人', '高坤林', '临期', '超期',
                        '处理', '生产日期', '袋装', '有货', '处理', '饲上', '单亲', '拆出', '价高', '勿扰', '美利', '低价', '两柜', '年份', '鼎牛',
                        '部位', '私聊', '猪肉', '发布', '货报', '一下', '一些', '相中来', '砍价', '国家', '粗修草', '四证齐', '重量', '厂全', '真空包装',
                        '好瘦', '预购', '从速', '超好', '文安', '联强', '食品', '装车', '打款', '定金', '辣椒', '拓鲜', '来报', '实惠', '公司', '平台',
                        '白杨', '新增', '美肥', '交流', '沟通', '系列产品', '大家', '交流', '沟通', '白杨', '客户', '价优', '奇货可居', '欲购从速', '还有',
                        '饲后', '来个', '需求', '不限厂', '接货', '内裙', '证件', '最后', '可以', '十吨', '缺失', '六月份', '装船', '档口', '现货供应',
                        '均码', '预计', '柜大码', '厂上', '厂龟', '特价', '能接', '中期', '三柜', '华后', '华去', '青白江', '明细', '请点', '普通',
                        '月底', '几个', '出入库', '六月', '中旬', '大码', '胴体', '大量', '生产', '板砖', '一吨', '换钱', '抵港', '实时', '七八件',
                        '多件', '可订', '囤货', '数柜', '暴涨', '李微', '信同', '五号', '厚群', '数吨', '两条', '小明', '没有', '马上', '龟建', '真空',
                        '船期', '七七','恒邦','厂冰鲜','五月','低于','冻品价']
        copy_word_list = copy.deepcopy(word_list)
        for i in word_list:
            pattern = re.compile('[a-zA-Z0-9]+')
            s = re.search(pattern, i)
            if s:
                copy_word_list.remove(i)
            elif '新货' == i or '带票' == i:
                copy_word_list.remove(i)
            elif '+' in i:
                copy_word_list.remove(i)
            elif '，' == i:
                copy_word_list.remove(i)
            elif i in area_list:
                copy_word_list.remove(i)
            elif i + '市' in area_list or i + '省' in area_list or i + '港' in area_list:
                copy_word_list.remove(i)
            elif i in rubbish_word:
                copy_word_list.remove(i)
            elif len(i) == 1:
                copy_word_list.remove(i)
        wfct = WFCT()
        for lw in copy_word_list:
            s3 = wfct.process_wfct(s1, lw)
        # 第一步：将信息按照数字进行切割
        # 拿到厂号所在位置的下标，注意是个元组
        if '-' in s3:
            dec_t_data = [(i.start(), i.end()) for i in re.finditer('((\d){1,2}-{1,2}(\d){1})', s3)]

        else:
            dec_t_data = [(i.start(), i.end()) for i in re.finditer('(\d{1,8})', s3)]

        for i in range(len(dec_t_data)):
            # 厂号
            changhao = s3[dec_t_data[i][0]:dec_t_data[i][1]]
            # 后续数据
            if i < len(dec_t_data) - 1 and s3[dec_t_data[i][1]:dec_t_data[i + 1][0]]:
                # 拿到厂号后面的数据
                d_data = s3[:dec_t_data[i][1]] + s3[dec_t_data[i][1]:dec_t_data[i + 1][0]]

                if '厂' in d_data:
                    d_data = d_data.replace('厂', '')
                if ' ' in d_data:
                    d_data = d_data.replace(' ', '，')
                if '、' in d_data:
                    d_data = d_data.replace(' ', '，')

                de_data = d_data.strip().split('，')

                # 最终去除'','/'的数据
                last_data = []

                for j in range(len(de_data)):
                    if de_data[j] == '' or de_data[j] == '/' or de_data[j] == '.' or de_data[j] == '+':
                        pass
                    else:
                        last_data.append(de_data[j])
                if last_data:
                    for p in range(len(last_data)):
                        for r in products:
                            for h in range(len(last_data[p])):
                                if last_data[p][h:h + 5] == r:
                                    item['changhao'] = changhao
                                    item['product'] = r

                                    for t in t_product:
                                        if item['product'] == t[0]:
                                            item['pid'] = t[1]
                                            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            print(item)
                                            print('*' * 100)
                                            if 'location' not in item.keys():
                                                item['location'] = ' '
                                            yield item

                                elif last_data[p][h:h + 4] == r:
                                    item['changhao'] = changhao
                                    item['product'] = r

                                    for t in t_product:
                                        if item['product'] == t[0]:
                                            item['pid'] = t[1]
                                            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            print(item)
                                            print('*' * 100)
                                            if 'location' not in item.keys():
                                                item['location'] = ' '
                                            yield item
                                elif last_data[p][h:h + 3] == r:
                                    item['changhao'] = changhao
                                    item['product'] = r

                                    for t in t_product:
                                        if item['product'] == t[0]:
                                            item['pid'] = t[1]
                                            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            print(item)
                                            print('*' * 100)
                                            if 'location' not in item.keys():
                                                item['location'] = ' '
                                            yield item
                                elif last_data[p][h:h + 3] + '肉' == r:
                                    item['changhao'] = changhao
                                    item['product'] = r

                                    for t in t_product:
                                        if item['product'] == t[0]:
                                            item['pid'] = t[1]
                                            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            print(item)
                                            print('*' * 100)
                                            if 'location' not in item.keys():
                                                item['location'] = ' '
                                            yield item

                                elif last_data[p][h:h + 2] in r and '/' not in r and last_data[p][
                                                                                     h:h + 2].isdigit() == False and len(
                                    last_data[p][h:h + 2]) != 1 and last_data[p][h:h + 2].isalpha() == False:
                                    item['changhao'] = changhao
                                    item['product'] = r
                                    for t in t_product:
                                        if item['product'] == t[0]:
                                            item['pid'] = t[1]
                                            item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            print(item)
                                            print('*' * 100)
                                            if 'location' not in item.keys():
                                                item['location'] = ' '
                                            yield item

    # 读取mysql中city的数据
    @staticmethod
    def read_mysql_city():
        mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
        data_cities = pd.read_sql('select * from d_bs_city;', con=mysql_cn)
        return list(data_cities['CITY_NAME'])

    @staticmethod
    def read_mysql_product1():
        mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
        data_product = pd.read_sql('select * from d_supply_product_class where pid !=0;', con=mysql_cn)
        return list(zip(data_product['class_name'], data_product['pid']))

    # 读取mysql中country的数据
    @staticmethod
    def read_mysql_country():
        mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
        data_cities = pd.read_sql('select * from d_country;', con=mysql_cn)
        return list(data_cities['name'])

    # 读取mysql中province的数据
    @staticmethod
    def read_mysql_province():
        mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
        data_cities = pd.read_sql('select * from d_bs_province;', con=mysql_cn)
        return list(data_cities['PROVINCE_NAME'])

    # 读取mysql中ods_supply_product_class中的数据
    @staticmethod
    def read_mysql_product():
        mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
        data_product = pd.read_sql('select * from d_supply_product_class where pid !=0;', con=mysql_cn)
        return list(data_product['class_name'])

# 做词库
class WFCT(object):
    def __init__(self):
        self.mysql_user = 'root'
        self.mysql_password = '123456'
        self.mysql_host = '127.0.0.1'
        self.mysql_database = 'lan'
        self.mysql_port = 3306
        self.redis_host = '127.0.0.1'
        self.redis_port = 6379
        self.redis_db = 1
        # 链接Redis数据库,db数据库默认连接到1
        self.redis_db = redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        # keys名字，里面的内容可以随便给，这里的keys相当于字典名称，而不是key值
        self.redis_data_dict = 'WFCT'
        # 链接MySQL数据库
        self.db = pymysql.connect(host=self.mysql_host, user=self.mysql_user, password=self.mysql_password,
                                  db=self.mysql_database,
                                  port=self.mysql_port, charset='utf8')
        self.cursor = self.db.cursor()

    # 添加词汇，并给当前的词汇赋初始值1
    def process_wfct(self, s3, word):
        # 判断Redis数据库中是否存在该词汇
        # hexists检查给定域中是否存与于哈希表中，若存在，则返回1，不存在则返回0
        if self.redis_db.hexists(self.redis_data_dict, word):
            # 这里表示Redis数据库中已存储了该词汇的字段
            # 那么如果再放该词汇的时候，该词汇的数值+1
            # 1. 先获取当前哈希表中存在的词汇的频数
            self.original_value = self.redis_db.hget(self.redis_data_dict, word)
            # 2. 在当前的基础上+1
            self.new_value = int(self.original_value) + 1
            # 3. 删除当前的词汇，否则无法进行插入
            self.redis_db.hdel(self.redis_data_dict, word)
            # 4. 重新放入
            self.redis_db.hset(self.redis_data_dict, word, self.new_value)
            # 5. 将当前的词汇及次数同步添加至MySQL数据库
            sql = 'update wordcount set frequency = %s where words=%s'
            self.cursor.execute(sql, (self.new_value, word))
            self.db.commit()
            return s3

        else:
            # 表示该词汇并没有被加入到Redis数据库，即该词汇是第一次出现
            # 将该词汇添加至Redis数据库，并给该词汇赋予值：1
            self.redis_db.hset(self.redis_data_dict, word, 1)
            # 同时将新产生的该词汇添加至MySQL数据库
            sql = 'insert into wordcount(words,frequency) values (%s,%s)'
            self.cursor.execute(sql, (word, 1))
            self.db.commit()
            return s3
