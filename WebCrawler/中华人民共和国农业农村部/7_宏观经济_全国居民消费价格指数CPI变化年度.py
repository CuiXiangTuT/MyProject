import random
from datetime import datetime

import requests
import redis
import pymysql

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
# 固定资产投资完成额变化
redis_dict_key = 'ods_cnncnybcpindbhqk'


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


def insertMysql(item):
    if redisDB.hexists(redis_dict_key,
                       item['ruralResidents'] + '-' + item['cityDweller'] + '-' + item[
                           'aquaticProducts'] + '-' + item['grain'] + '-' + item['freshFruits']):
        print('已存在该值，不作处理...')
    else:
        redisDB.hset(redis_dict_key, item['ruralResidents'] + '-' + item['cityDweller'] + '-' + item[
            'aquaticProducts'] + '-' + item['grain'] + '-' + item['freshFruits'], 0)
        sql = 'insert into ods_chinanongcunnongyebucpindbhqk(classification,ruralResidents,cityDweller,aquaticProducts,grain,eggs,freshFruits,freshVegetables,totalIndex,Ctime,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (item['classification'],
                             item['ruralResidents'], item['cityDweller'], item['aquaticProducts'], item['grain'],
                             item['eggs'], item['freshFruits'], item['freshVegetables'], item['totalIndex'],
                             item['Ctime'],
                             item['insertTime']))
        print('正在插入数据，请稍等...')
        conn.commit()


def getData():
    url = 'http://zdscxx.moa.gov.cn:8080/nyb/qgjmxfjgzs'
    item = {}
    headers = {
        'Referer': 'http://zdscxx.moa.gov.cn:8080/nyb/pc/index.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'item': '年度'
    }
    item['classification'] = '年度'
    ip = random.choice(ipList)
    response = requests.post(url=url, headers=headers, data=data,
                             proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['result']['rowDatas']
    for perData in response:
        try:
            # 农村居民
            item['ruralResidents'] = perData['#农村居民']
        except:
            item['ruralResidents'] = ''
        try:
            # 城市居民
            item['cityDweller'] = perData['#城市居民']
        except:
            item['cityDweller'] = ''
        try:
            # 水产品类
            item['aquaticProducts'] = perData['#水产品类']
        except:
            item['aquaticProducts'] = ''
        try:
            # 粮食类
            item['grain'] = perData['#粮食类']
        except:
            item['grain'] = ''
        try:
            # 蛋类
            item['eggs'] = perData['#蛋类']
        except:
            item['eggs'] = ''
        try:
            # 鲜果类
            item['freshFruits'] = perData['#鲜果类']
        except:
            item['freshFruits'] = ''
        try:
            # 鲜菜类
            item['freshVegetables'] = perData['#鲜菜类']
        except:
            item['freshVegetables'] = ''
        try:
            # 总指数
            item['totalIndex'] = perData['总指数']
        except:
            item['totalIndex'] = ''
        try:
            # 时间
            item['Ctime'] = perData['时间']
        except:
            item['Ctime'] = ''
        # 插入时间
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insertMysql(item)


if __name__ == '__main__':
    ipList = getIp()
    getData()
    cursor.close()
    conn.close()
