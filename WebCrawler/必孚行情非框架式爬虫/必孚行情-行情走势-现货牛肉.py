import json
import random
from datetime import datetime
from pprint import pprint

import pymysql
import redis
import requests

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redis_db = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_data_dict = 'ods_bifu_hangqingzoushi_niurou'


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
                        item['country'] + '-' + item['part'] + '-' + item['publishTime'] + '-' + item['rise']+ '-' + item['goodsType']):
        # 若存在，输出数据库已经存在该数据
        print('数据库中已经存在该数据,不做处理~~~')

    else:
        print('正在入库，请稍等~~~')
        # 若不存在，则将URL写入Redis数据库中
        # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
        redis_db.hset(redis_data_dict, item['country'] + '-' + item['part'] + '-' + item['publishTime'] + '-' + item['rise']+ '-' + item['goodsType'],
                      0)
        # 进行MySQL入库处理
        sql = 'insert into ods_bifu_hangqingzoushi_niurou(country,part,feedingMode,publishTime,keyWord,rise,goodsType,goodsPrice,unit,quotationType,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['country'], item['part'], item['feedingMode'], item['publishTime'], item['keyWord'], item['rise'],item['goodsType'],item['goodsPrice'],item['unit'],item['quotationType'],
            item['insertTime']))
        conn.commit()


def getData():
    item = {}
    feedingModes = ['谷饲', '草饲']
    country = ['澳大利亚', '巴西']
    parts = ['板腱', '牛腩80vl']
    # 货物类型
    item['goodsType'] = '现货'
    zipData = list(zip(feedingModes, country, parts))
    for per_zip in zipData:
        url = 'https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceDataIndex'
        headers = {
            'referer': 'https://www.beeftochina.com.cn/cn/BTCPrice',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
            'x-token': '24908574-bf80-46ba-b572-991e6c567b43',
        }
        data = {"MessageID": "839d4cea-630e-4b5e-beb9-d71a646edc02", "MessageType": 3000000004,
                "Data": {"UserID": "danaodaiyangyang", "Part": per_zip[2], "Country": per_zip[1], "Parts": [per_zip[2]],
                         "Countries": [per_zip[1]], "RecommendDay": 0, "FeedingMode": per_zip[0], "Type": "_spotgoods",
                         "IsFirst": True,
                         "IsEn": False}}
        ip = random.choice(ipList)
        response = requests.post(url=url, headers=headers, json=data,
                                 proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()
        riseList = response['Data']['Row']['riseList'][0]
        categories = response['Data']['Row']['categories']
        series = response['Data']['Row']['series'][0]['data']

        zipList = list(zip(riseList, categories, series))
        # 国家
        item['country'] = per_zip[1]
        # 部位
        item['part'] = per_zip[2]
        # 饲养方式
        item['feedingMode'] = per_zip[0]
        for perZip in zipList:
            # 时间
            item['publishTime'] = perZip[1]
            # 关键字
            item['keyWord'] = perZip[0]['key']
            # 增长率
            item['rise'] = perZip[0]['rise']
            # 价格
            item['goodsPrice'] = perZip[2]
            # 单位
            item['unit'] = '元/公斤'
            # 行情类型
            item['quotationType'] = '牛肉'
            # 插入时间
            item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insertMysql(item)
            print(item)


if __name__ == '__main__':
    ipList = getIp()
    getData()
    cursor.close()
    conn.close()
