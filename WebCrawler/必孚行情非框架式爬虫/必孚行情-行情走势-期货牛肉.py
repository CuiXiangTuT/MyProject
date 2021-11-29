import random
from datetime import datetime

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
    url = 'https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceDataIndex'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
    }
    jsonData = {"MessageID": "8315ca63-753a-45b4-8b52-860314ea17df", "MessageType": 3000000004,
                "Data": {"UserID": "danaodaiyangyang", "Part": "牛腩80vl", "Country": "巴西", "Parts": ["牛腩80vl"],
                         "Countries": ["巴西"], "RecommendDay": 0, "FeedingMode": "草饲", "Type": "_futures",
                         "IsFirst": True, "IsEn": False}}
    # 国家
    item['country'] = '巴西'
    # 部位
    item['part'] = '牛腩80vl'
    # 饲养方式
    item['feedingMode'] = '草饲'
    # 货物类型
    item['goodsType'] = '期货'
    ip = random.choice(ipList)
    response = requests.post(url=url, headers=headers,json=jsonData,proxies={'http':'http://'+ ip['ip'] + ':' + ip['port']}).json()
    categories = response['Data']['Row']['categories']
    riseList = response['Data']['Row']['riseList'][0]
    series = response['Data']['Row']['series'][0]['data']
    zipList = list(zip(categories,riseList,series))
    for perZip in zipList:
        # 时间
        item['publishTime'] = perZip[0]
        # 关键词
        item['keyWord'] = perZip[1]['key']
        # 增长率
        item['rise'] = perZip[1]['rise']
        # 价格
        item['goodsPrice'] = perZip[2]
        # 单位
        item['unit'] = '美元/吨'
        # 行情类型
        item['quotationType'] = '牛肉'
        # 插入时间
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(item)
        insertMysql(item)

if __name__ == '__main__':
    ipList = getIp()
    getData()
    cursor.close()
    conn.close()

