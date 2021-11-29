import random
import re
from datetime import datetime

import pymysql
import redis
import requests
import pandas as pd
import numpy as np

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redis_db = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_data_dict = 'ods_bifu_hangqingzoushi_huoniu'


# 获取讯代理IP
def getIp():
    xdl_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=913d4f4b67e24be0998a3eb344ff732b&orderno=YZ2021923652gUFZCj&returnType=2&count=10'
    ipListData = requests.get(url=xdl_url).json()
    ipList = []
    ipList.clear()
    # 将ip以字典的形式添加至ip池
    for everyIp in ipListData['RESULT']:
        ipList.append({
            'ip': everyIp['ip'],
            'port': everyIp['port']
        })
    return ipList


# 插入数据
def insertMysql(item):
    if redis_db.hexists(redis_data_dict,
                        item['country'] + '-' + item['keyWord'] + '-' + str(item['goodsPrice']) + '-' + str(item['rise'])):
        # 若存在，输出数据库已经存在该数据
        print('数据库中已经存在该数据,不做处理~~~')

    else:
        print('正在入库，请稍等~~~')
        # 若不存在，则将URL写入Redis数据库中
        # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
        redis_db.hset(redis_data_dict,
                      item['country'] + '-' + item['keyWord'] + '-' + str(item['goodsPrice']) + '-' + str(item['rise']),
                      0)
        # 进行MySQL入库处理
        sql = 'insert into ods_bifu_hangqingzoushi_huoniu(country,keyWord,goodsSort,goodsPrice,rise,publishTime,unit,quotationType,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['country'], item['keyWord'], item['goodsSort'], item['goodsPrice'], item['rise'], item['publishTime'],
            item['unit'], item['quotationType'],
            item['insertTime']))
        conn.commit()


def getData():
    countries = ['美国', '巴西', '澳大利亚', '乌拉圭', '阿根廷']
    item = {}
    i = 0
    for country in countries:
        url = 'https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceLivecattleIndex'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
        }
        jsonData = {"MessageID": "c3bd2d87-ffde-43fa-8830-4120d5cbfb4f", "MessageType": 3000000005,
                    "Data": {"UserID": "danaodaiyangyang", "Country": country, "isEn": False}}
        ip = random.choice(ipList)
        response = requests.post(url=url, headers=headers, json=jsonData,
                                 proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['Data']['Row']

        if country == '美国':
            categories = response['categories']
            riseList = response['riseList'][0]
            series = response['series'][0]['data']
            zipList = list(zip(categories, riseList, series))
            for per_zip in zipList:
                # 时间
                item['publishTime'] = per_zip[0]
                # 关键词
                item['keyWord'] = per_zip[1]['key']
                # 增长率
                item['rise'] = per_zip[1]['rise']
                # 价格
                item['goodsPrice'] = per_zip[2]
                # 单位
                item['unit'] = "美元/kg lwt"
                # 国家
                item['country'] = country
                # 品类
                item['goodsSort'] = '活牛'
                # 行情类型
                item['quotationType'] = '活牛'
                # 插入时间
                item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(item)
                insertMysql(item)
        else:
            riseList_1 = response['riseList'][0]
            riseList_2 = response['riseList'][1]
            series_1 = response['series'][0]['data']
            series_2 = response['series'][1]['data']
            riseList = riseList_1 + riseList_2
            keyList = [item['key'] for item in riseList]
            risePersentList = [item['rise'] for item in riseList]
            series = series_1 + series_2
            df = pd.DataFrame(np.mat([series, keyList, risePersentList]).T,
                              columns=['goodsPrice', 'keyWord', 'rise'])
            pattern_time = re.compile('\d{4}-\d{2}-\d{2}')
            for i in range(len(df)):
                # 时间
                publishKey = df.iloc[i]['keyWord']
                item['publishTime'] = re.findall(pattern=pattern_time, string=publishKey)[0]
                # 关键词
                item['keyWord'] = publishKey
                # 品类
                item['goodsSort'] = publishKey.split('-')[0]
                # 增长率
                item['rise'] = df.iloc[i]['rise']
                # 价格
                item['goodsPrice'] = df.iloc[i]['goodsPrice']
                # 单位
                if country == '巴西':
                    item['unit'] = ''
                else:
                    item['unit'] = 'USD/kg lwt'
                # 国家
                item['country'] = country
                # 行情类型
                item['quotationType'] = '活牛'
                # 插入时间
                item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(item)
                insertMysql(item)


if __name__ == '__main__':
    ipList = getIp()
    getData()
