from datetime import datetime

import requests
import random
import pymysql
import redis

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'nongmurenxiaodian'


def getIpList():
    ipList = []
    ipUrl = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=913d4f4b67e24be0998a3eb344ff732b&orderno=YZ2021923652gUFZCj&returnType=2&count=10'
    ipResponse = requests.get(url=ipUrl).json()["RESULT"]
    for everyIp in ipResponse:
        ipList.append({
            'ip': everyIp['ip'],
            'port': everyIp['port']
        })
    return ipList


def insertMysql(item):
    if redisDB.hexists(redis_dict_key, item['shopName'] + '-' + item['province'] + '-' + item['city'] + '-' + item[
        'addressInfo'] + '-' + item['shopCode']):
        print('此数据已存在，不做处理~~~')
    else:
        print('数据正在入库...')
        print('-'*50)
        redisDB.hset(redis_dict_key,
                     item['shopName'] + '-' + item['province'] + '-' + item['city'] + '-' + item['addressInfo'] + '-' +
                     item['shopCode'], 0)
        sql = 'insert into ods_nongmurenxiaodian(shopName,province,provinceId,city,cityId,addressInfo,area,areaId,shopAddress,shopCode,businessBody,categoryName,goodsName,legalPerson,shopPeople,shopPhone,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (item['shopName'], item['province'], item['provinceId'], item['city'], item['cityId'],
                       item['addressInfo'], item['area'], item['areaId'], item['shopAddress'], item['shopCode'],
                       item['businessBody'], item['categoryName'], item['goodsName'], item['legalPerson'],
                       item['shopPeople'], item['shopPhone'], item['insertTime']))
        conn.commit()


def getData(ipList):
    url = 'https://pay.nongmuren.com/nongMuRenZGTSec/applets/homePage/getNearbySelfHzShopList'
    headers = {
        "Host": "pay.nongmuren.com",
        "Connection": "keep-alive",
        "Content-Length": "57",
        "Authorization": "",
        "FROM_TYPE": "3",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        "content-type": "application/json",
        "custom-header": "application/x-www.form-urlencoded",
        "Referer": "https://servicewechat.com/wx18afa348e55fc802/15/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
    }
    for pageNum in range(1, 30):
        proxyIP = random.choice(ipList)
        data = {"lat": 39.9219, "lng": 116.44355, "pageNum": pageNum, "pageSize": 10}
        response = requests.post(url=url, headers=headers, json=data,
                                 proxies={'http': str(proxyIP['ip']) + ":" + str(proxyIP['port'])}).json()['data'][
            'list']

        item = {}
        for everyShop in response:
            try:
                # 商店名
                item['shopName'] = everyShop['selfShopHomePageRedis']['shopRedis']['shopName']
            except:
                item['shopName'] = ''
            try:
                # 省份
                item['province'] = everyShop['selfShopHomePageRedis']['shopRedis']['province']
            except:
                item['province'] = ''
            try:
                # 省份id
                item['provinceId'] = everyShop['selfShopHomePageRedis']['shopRedis']['provinceId']
            except:
                item['provinceId'] = ''
            try:
                # 城市
                item['city'] = everyShop['selfShopHomePageRedis']['shopRedis']['city']
            except:
                item['city'] = ''
            try:
                # 城市id
                item['cityId'] = everyShop['selfShopHomePageRedis']['shopRedis']['cityId']
            except:
                item['cityId'] = ''
            try:
                # 地址
                item['addressInfo'] = everyShop['selfShopHomePageRedis']['shopRedis']['addressInfo']
            except:
                item['addressInfo'] = ''
            try:
                # 地区
                item['area'] = everyShop['selfShopHomePageRedis']['shopRedis']['area']
            except:
                item['area'] = ''
            try:
                # 地区id
                item['areaId'] = everyShop['selfShopHomePageRedis']['shopRedis']['areaId']
            except:
                item['areaId'] = ''
            try:
                # 商店地址
                item['shopAddress'] = everyShop['selfShopHomePageRedis']['shopRedis']['shopAddress']
            except:
                item['shopAddress'] = ''
            try:
                # 商店编码
                item['shopCode'] = everyShop['selfShopHomePageRedis']['shopRedis']['shopCode']
            except:
                item['shopCode'] = ''
            try:
                # 生意
                item['businessBody'] = everyShop['selfShopHomePageRedis']['shopRedis']['businessBody']
            except:
                item['businessBody'] = ''
            try:
                # 类型名
                item['categoryName'] = everyShop['selfShopHomePageRedis']['shopRedis']['categoryName']
            except:
                item['categoryName'] = ''
            try:
                # 商品名
                item['goodsName'] = everyShop['selfShopHomePageRedis']['shopRedis']['goodsName']
            except:
                item['goodsName'] = ''
            try:
                # 合法人
                item['legalPerson'] = everyShop['selfShopHomePageRedis']['shopRedis']['legalPerson']
            except:
                item['legalPerson'] = ''
            try:
                # 店主
                item['shopPeople'] = everyShop['selfShopHomePageRedis']['shopRedis']['shopPeople']
            except:
                item['shopPeople'] = ''
            try:
                # 联系方式
                item['shopPhone'] = everyShop['selfShopHomePageRedis']['shopRedis']['shopPhone']
            except:
                item['shopPhone'] = ''

            item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insertMysql(item)


if __name__ == '__main__':
    ipList = getIpList()
    getData(ipList)
