from datetime import datetime

import scrapy
from ..items import ZhongguonongyebushujuchaxundadouItem


class ZgnybsjcxddSpider(scrapy.Spider):
    name = 'zgnybsjcxdd'
    allowed_domains = ['http://zdscxx.moa.gov.cn/']
    start_urls = ['http://http://zdscxx.moa.gov.cn//']

    def start_requests(self):
        item = ZhongguonongyebushujuchaxundadouItem()
        # 地区列表
        areaList = ['', '全球', '全球平均', '全国', '北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽',
                    '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃',
                    '青海', '宁夏', '新疆', '全国(省份平均)']

        # 数据来源
        sourceList = ['', '国家发展改革委', '农业农村部市场与信息化司', '海关总署', '国家统计局', '联合国粮农组织', '农业农村部农业机械化管理司', '农业农村部渔业渔政局',
                      '郑州商品交易所、大连商品交易所', '农业农村部300个价格监测网点县', '大米泰国离岸价(5%破碎率)，小麦、玉米、大豆为芝加哥商品交易所期货价。', '中国饲料工业协会',
                      '农业农村部科技教育司、种植业管理司、农业机械化管理司、信息中心', '豆油为芝加哥商品交易所期货价，棕榈油为马来西亚下两个月船期离岸价，菜籽油欧洲市场FOB报价。(单位:欧元/吨)']

        # 指标名称
        indexList = ['', '每亩化肥金额_其他肥料', '产量', '每亩化肥折纯用量_钾肥', '每亩化肥金额_氮肥', '每50公斤主产品现金成本', '每亩修理维护费', '每亩管理费', '每亩水费',
                     '每亩化肥金额_二铵', '每50公斤主产品净利润', '每亩自营地折租', '每亩燃料动力费', '每亩土地成本', '每亩现金成本', '每亩生产成本(按统一工价)', '每亩化肥金额_总',
                     '每亩雇工天数', '种籽秧苗用量', '每亩租赁作业费', '每亩农药费', '每亩化肥金额_磷肥', '每亩家庭用工天数', '每亩化肥金额_复混肥', '每亩化肥金额_尿素',
                     '每亩劳动日工价', '每50公斤主产品平均出售价格', '每亩人工成本', '每亩副产品产值', '每亩主产品出售产值', '每亩化肥费', '每亩机械作业费',
                     '每50公斤主产品生产成本(按统一工价)', '每亩主产品出售数量', '每亩现金收益', '每亩化肥金额_过磷酸钙', '累计出口金额', '累计进口金额', '累计出口数量',
                     '累计进口数量', '当月进口数量', '每亩化肥金额_复合肥', '当月出口数量', '当月出口金额', '每亩化肥金额_混配肥', '每亩化肥金额_钾肥', '每亩雇工工价',
                     '每亩化肥折纯用量_碳铵', '播种面积', '每亩物质与服务费用', '每亩化肥折纯用量_复混肥', '每亩化肥折纯用量_二铵', '每亩化肥金额_三元素复合肥', '每亩化肥折纯用量_磷肥',
                     '每50公斤主产品现金收益', '每亩农家肥费', '每亩化肥折纯用量_复合肥', '每亩产值合计', '每亩固定资产折旧', '每亩家庭用工折价', '机械化率', '每亩净利润',
                     '每亩化肥折纯用量_尿素', '每亩化肥金额_碳铵', '每亩主产品产值', '每亩用工数量', '每亩化肥用量', '每50公斤主产品总成本', '每亩工具材料费', '每亩销售费',
                     '每亩排灌费', '每亩直接费用', '每亩主产品产量', '每亩雇工费用', '每亩种籽秧苗费', '每亩间接费用', '每亩成本利润率', '每亩化肥折纯用量_过磷酸钙', '每亩流转地租金',
                     '每亩畜力费', '每亩化肥折纯用量_总', '每亩化肥折纯用量_氯化钾', '每亩化肥折纯用量_混配肥', '每亩保险费', '每亩成本外支出', '当月进口金额', '亩化肥金额_氯化钾',
                     '每亩总成本', '收购价', '期货价', '市场价']

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
                                    'tag': '{"content":"农业统计信息","table":"COMMON_FACT","product":["大豆机收率##主要作物农机作业水平##农业投入品","大豆##粮食##价格","大豆耕种收综合机械化率##主要作物农机作业水平##农业投入品","大豆##粮食##农业生产","大豆(大商所)##豆类##价格","大豆##国际粮食价格##价格","大豆(美国CBOT)##豆类##价格","大豆##种植业##进出口贸易","大豆##蔬菜##农业生产","大豆##粮食(粮经作物)##成本收益","大豆机播率##主要作物农机作业水平##农业投入品","大豆机耕率##主要作物农机作业水平##农业投入品"],"item":["每亩种籽秧苗费","3月期价","每亩主产品产值","每亩化肥金额_钾肥","每亩机械作业费","每亩主产品出售产值","每亩雇工费用","每亩化肥折纯用量_碳铵","每亩直接费用","每亩总成本","每亩化肥金额_复合肥","每亩化肥折纯用量_氯化钾","每亩雇工天数","每亩化肥金额_尿素","每亩主产品出售数量","每亩化肥金额_磷肥","每亩主产品产量","每亩化肥金额_混配肥","每亩排灌费","8月期价","每50公斤主产品现金成本","每亩化肥折纯用量_尿素","11月期价","当月进口数量","每亩化肥折纯用量_混配肥","每亩土地成本","每亩净利润","每亩化肥折纯用量_钾肥","每亩销售费","每亩现金收益","每亩租赁作业费","每亩化肥金额_氮肥","每亩雇工工价","每亩间接费用","每亩管理费","每亩燃料动力费","每亩生产成本(按统一工价)","每亩水费","每亩用工数量","当月出口数量","9月期价","累计进口数量","每亩成本外支出","收购价","每亩人工成本","每50公斤主产品现金收益","每亩化肥用量","每亩化肥折纯用量_总","每亩化肥费","当月出口金额","每亩成本利润率","每50公斤主产品总成本","7月期价","每亩化肥折纯用量_复合肥","每亩家庭用工折价","每亩流转地租金","每亩化肥折纯用量_复混肥","每亩化肥金额_过磷酸钙","累计进口金额","每50公斤主产品平均出售价格","每亩化肥金额_其他肥料","每亩农家肥费","机械化率","亩化肥金额_氯化钾","每亩化肥金额_三元素复合肥","每亩化肥金额_二铵","市场价","当月进口金额","期货价","每亩修理维护费","每亩化肥折纯用量_二铵","产量","每亩副产品产值","每50公斤主产品生产成本(按统一工价)","每亩现金成本","每亩家庭用工天数","播种面积","累计出口数量","1月期价","每亩保险费","5月期价","每亩化肥金额_总","每亩化肥金额_碳铵","每亩化肥金额_复混肥","每亩化肥折纯用量_磷肥","每亩农药费","每亩劳动日工价","DCE连续期货价格","每亩自营地折租","每亩化肥折纯用量_过磷酸钙","每亩产值合计","每亩物质与服务费用","每亩固定资产折旧","CBOT连续期货价格","每亩畜力费","种籽秧苗用量","每亩工具材料费","累计出口金额","每50公斤主产品净利润"],"area":["湖北","广西","甘肃","陕西","上海","重庆","河南","北京","吉林","河北","宁夏","山西","福建","江西","西藏","安徽","云南","全国","海南","湖南","天津","全球","青海","全球平均","四川","江苏","内蒙古","全国(省份平均)","贵州","广东","黑龙江","山东","辽宁","新疆","浙江"],"keyWord":"大豆"}',
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
