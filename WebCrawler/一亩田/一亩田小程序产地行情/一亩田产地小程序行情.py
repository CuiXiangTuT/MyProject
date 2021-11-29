import datetime
import json
import random
import time
import uuid
import re

import pymysql
import redis
import requests

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redis_db = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_data_dict = 'ods_ymt_xiaochengxuchandihangqing'


# 1.获取讯代理IP
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


# 4.插入到数据库
def insertMysql(item):
    if redis_db.hexists(redis_data_dict,
                        str(item['product']) + '-' + str(item['Cid']) + '-' + str(
                            item['breedId']) + '-' + str(item['main_loc_id']) + '-' + str(
                            item['Cname']) + '-' + str(item['price'])):
        # 若存在，输出数据库已经存在该数据
        print('数据库中已经存在该数据,不做处理~~~')

    else:
        print('正在入库，请稍等~~~')
        # 若不存在，则将URL写入Redis数据库中
        # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
        redis_db.hset(redis_data_dict,
                      str(item['product']) + '-' + str(item['Cid']) + '-' + str(
                          item['breedId']) + '-' + str(item['main_loc_id']) + '-' + str(
                          item['Cname']) + '-' + str(item['price']), 0)
        # 进行MySQL入库处理
        sql = 'insert into ods_ymt_xiaochengxuhangqing(product,Cid,productId,trend,price,breedId,location,main_loc_id,Cname,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['product'], item['Cid'], item['productId'], item['trend'], item['price'], item['breedId'],
            item['location'], item['main_loc_id'], item['Cname'], item['insertTime']))
        conn.commit()


# 3.分段获取数据
def getData(resList):
    fontPattern = re.compile("font color=.*?>(.*?)<")
    for everyRes in resList:
        # id
        item['Cid'] = everyRes['id']
        # 产品id
        item['productId'] = everyRes['product_id']
        # 变化情况
        trend = everyRes['trend']
        if 'font' in trend:
            item['trend'] = re.findall(pattern=fontPattern, string=trend)[0]
        else:
            item['trend'] = trend
        # 价格
        price = everyRes['price']
        if 'font' in price:
            item['price'] = re.findall(pattern=fontPattern, string=price)[0]
        else:
            item['price'] = price
        # 品种识别号
        item['breedId'] = everyRes['breed_id']
        # 地址
        item['location'] = everyRes['location']
        # 主站点id
        item['main_loc_id'] = everyRes['main_loc_id']
        # 产品
        item['Cname'] = everyRes['name']
        # 插入时间
        item['insertTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(item)
        insertMysql(item)


# 2.获取内容
def getPageData():
    for pageNum in range(1, 50):
        url = 'https://webgfw2.ymt.com/price/v13/market/origin_market?ts={}&fCode=1000002&version=2.15.11'.format(
            time.time() * 10000000)
        headers = {
            'Host': 'webgfw2.ymt.com',
            # 'Connection': 'keep-alive',
            'Content-Length': '68',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
            'X-App-UUID': str(uuid.uuid4()).replace('-', ''),
            'X-App-Version': '2.15.11',
            'X-Encode': '0',
            'X-User-Agent': '2006',
            'content-type': 'application/json',
            'Referer': 'https://servicewechat.com/wx2fa4f48c3632092f/79/page-frame.html',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        for product_id in [489012, 489015]:
            jsonData = {
                "breed_id": -1,
                "index": pageNum,
                "length": 10,
                "product_id": product_id,
                "query": ""
            }
            if product_id == 489012:
                item['product'] = '羊产品'
            else:
                item['product'] = '牛产品'
            randomIp = random.choice(ipList)
            resList = requests.post(url=url, headers=headers, data=json.dumps(jsonData),
                                    proxies={"http": 'http://' + str(randomIp['ip']) + ':' + randomIp['port']}).json()[
                'result']['list']
            getData(resList)


if __name__ == '__main__':
    item = {}
    ipList = getIp()
    getPageData()
