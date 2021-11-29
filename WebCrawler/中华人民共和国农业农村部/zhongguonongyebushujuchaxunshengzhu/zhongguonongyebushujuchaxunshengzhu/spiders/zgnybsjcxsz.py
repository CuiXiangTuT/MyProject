from datetime import datetime

import scrapy
from ..items import ZhongguonongyebushujuchaxunshengzhuItem


class ZgnybsjcxszSpider(scrapy.Spider):
    name = 'zgnybsjcxsz'
    allowed_domains = []

    # start_urls = ['http://http://zdscxx.moa.gov.cn:8080//']

    def start_requests(self):
        item = ZhongguonongyebushujuchaxunshengzhuItem()
        # 地区列表
        areaList = ['', '全国', '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西',
                    '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '陕西', '甘肃', '青海', '宁夏', '新疆',
                    '全国(省份平均)']

        # 数据来源
        sourceList = ['', '国家发展改革委', '国家统计局、农业农村部畜牧兽医局', '海关总署', '国家统计局']

        # 指标名称
        indexList = ['', '每50公斤主产品总成本', '每头(或百只)物质与服务费用', '每头(或百只)医疗防疫费', '每核算单位用工数量', '每头(或百只)销售费', '每50公斤主产品净利润',
                     '出栏量', '每50公斤主产品平均出售价格', '每头(或百只)直接费用', '每头(或百只)人工成本', '每头(或百只)生产成本(按统一工价)', '平均饲养天数',
                     '每头(或百只)死亡损失费', '每头(或百只)家庭用工折价', '每头(或百只)工具材料费', '每头(或百只)劳动日工价', '每头(或百只)雇工费用', '每头(或百只)修理维护费',
                     '每头(或百只)仔畜进价', '每头(或百只)精饲料费', '每50公斤主产品生产成本(按统一工价)', '每头(或百只)主产品产量', '当月出口数量', '累计出口数量', '当月出口金额',
                     '累计进口金额', '累计出口金额', '累计进口数量', '每头(或百只)主产品产值', '当月进口数量', '每头(或百只)管理费', '每头(或百只)电费', '每头(或百只)水费',
                     '每头(或百只)副产品产值', '耗粮数量', '每头(或百只)燃料动力费', '每头(或百只)固定资产折旧', '精饲料数量', '每头(或百只)总成本', '每头(或百只)产值合计',
                     '每头(或百只)煤费', '每头(或百只)财务费', '每头(或百只)保险费', '每头(或百只)间接费用', '当月进口金额', '每头(或百只)雇工工价', '每头(或百只)青粗饲料费',
                     '每头(或百只)雇工天数', '每头(或百只)其他直接费用', '每头(或百只)净利润', '每头(或百只)成本利润率', '每头(或百只)饲料加工费', '仔畜重量',
                     '每头(或百只)土地成本', '每头(或百只)家庭用工天数', '每头(或百只)技术服务费', '每头(或百只)其它燃料动力费', '存栏量']

        for perArea in areaList:
            for perSource in sourceList:
                for perIndex in indexList:
                    for pageNum in range(1, 30):
                        try:
                            url = 'http://zdscxx.moa.gov.cn:8080/nyb/getHotWordData'
                            headers = {
                                'Referer': 'http://zdscxx.moa.gov.cn:8080/nyb/pc/search.jsp',
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                                'X-Requested-With': 'XMLHttpRequest',
                            }
                            data = {'page': str(pageNum),
                                    'rows': '20',
                                    'tag': '{"content":"农业统计信息","table":"COMMON_FACT","product":["中规模生猪##畜禽产品(肉、禽、蛋、奶,畜产品)##成本收益","生猪##畜产品##农业生产","生猪(大商所)##猪产品##价格","生猪##养殖业##进出口贸易","大规模生猪##畜禽产品(肉、禽、蛋、奶,畜产品)##成本收益","散养生猪##畜禽产品(肉、禽、蛋、奶,畜产品)##成本收益","小规模生猪##畜禽产品(肉、禽、蛋、奶,畜产品)##成本收益"],"item":["每50公斤主产品平均出售价格","3月期价","出栏量","每头(或百只)土地成本","累计出口数量","存栏量","每头(或百只)饲料加工费","每头(或百只)成本利润率","仔畜重量","1月期价","每头(或百只)家庭用工天数","每头(或百只)直接费用","精饲料数量","每头(或百只)青粗饲料费","5月期价","累计进口金额","每头(或百只)劳动日工价","每头(或百只)固定资产折旧","每头(或百只)雇工费用","累计出口金额","每头(或百只)其它燃料动力费","每头(或百只)燃料动力费","每头(或百只)医疗防疫费","平均饲养天数","每头(或百只)工具材料费","每头(或百只)精饲料费","每头(或百只)生产成本(按统一工价)","每50公斤主产品净利润","每头(或百只)水费","耗粮数量","每头(或百只)雇工工价","每头(或百只)净利润","每头(或百只)技术服务费","每头(或百只)管理费","每头(或百只)家庭用工折价","当月出口数量","当月进口金额","每核算单位用工数量","每头(或百只)总成本","累计进口数量","每头(或百只)死亡损失费","每头(或百只)电费","9月期价","每头(或百只)财务费","DCE连续期货价格","每头(或百只)销售费","每头(或百只)保险费","每头(或百只)其他直接费用","每头(或百只)修理维护费","每头(或百只)副产品产值","11月期价","每50公斤主产品生产成本(按统一工价)","每头(或百只)产值合计","当月出口金额","每50公斤主产品总成本","7月期价","当月进口数量","每头(或百只)仔畜进价","每头(或百只)主产品产值","每头(或百只)人工成本","每头(或百只)主产品产量","每头(或百只)煤费","每头(或百只)雇工天数","每头(或百只)间接费用","每头(或百只)物质与服务费用"],"area":["湖北","广西","甘肃","陕西","上海","重庆","河南","山西","吉林","北京","江西","河北","福建","宁夏","安徽","云南","海南","全国","湖南","天津","青海","四川","江苏","内蒙古","全国(省份平均)","贵州","广东","黑龙江","辽宁","山东","新疆","浙江"],"keyWord":"生猪"}',
                                    'level': '',
                                    'time': '["2017-09-07","2021-09-07"]',
                                    'product': '',
                                    'item': perIndex,
                                    'area': perArea,
                                    'source': perSource,
                                    'format': ''
                                    }
                            # 地区
                            item['Carea'] = perArea
                            # 来源
                            item['Csource'] = perSource
                            # 指标名称
                            item['CindexName'] = perIndex
                            yield scrapy.FormRequest(url=url, headers=headers, callback=self.parse,
                                                     dont_filter=True,
                                                     formdata=data, meta={'item': item})
                        except:
                            pass


    def parse(self, response):
        item = response.meta['item']
        jsonDataList = response.json()['result']['pageInfo']['table']
        for perJsonData in jsonDataList:
            try:
                # 时间
                item['Ctime'] = perJsonData['time']
            except:
                item['Ctime'] = ''
            try:
                # 品类
                item['product'] = perJsonData['product']
            except:
                item['product'] = ''
            try:
                # 指标名称
                item['itemName'] = perJsonData['item']
            except:
                item['itemName'] = ''
            try:
                # 指标类型
                item['itemType'] = perJsonData['item_type']
            except:
                item['itemType'] = ''
            try:
                # 地区
                item['area'] = perJsonData['area']
            except:
                item['area'] = ''
            try:
                # 周期
                item['Cperiod'] = perJsonData['period']
            except:
                item['Cperiod'] = ''
            try:
                # 单位
                item['unit'] = perJsonData['unit']
            except:
                item['unit'] = ''
            try:
                # 数值
                item['Cvalue'] = perJsonData['value']
            except:
                item['Cvalue'] = ''
            # 插入时间
            item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
