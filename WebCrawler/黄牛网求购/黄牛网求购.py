import pymysql
import redis
import requests

conn = pymysql.Connect(host='10.10.107.7', user='root', database='bigdata', password='xinqian@saibao', port=3306)
cursor = conn.cursor()

redis_db = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_data_dict = 'hnw_qiugou'

url = 'http://www.chinahuangniu.com/portal-api/pendingOrder/platform/demand/getCustPage?pageSize=20&pageNum=1&createDateSort=&maxCount=&minCount=&minUnitPrice=&maxUnitPrice=&deliveryPeriod='
headers = {
    "Referer": "http://www.chinahuangniu.com/html/sale/requirement.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
json_data_list = requests.get(url=url, headers=headers).json()['data']['list']
item = {}
for eve_data in json_data_list:
    # 商品名称
    item['orderTitle'] = eve_data['orderTitle']
    # 价格范围最小值
    item['minNakedPrice'] = eve_data['minNakedPrice']
    # 价格范围最大值
    item['maxNakedPrice'] = eve_data['maxNakedPrice']
    # 牛需求数量
    item['totalCount'] = eve_data['totalCount']
    # 交割日期
    item['deliveryPeriod'] = eve_data['deliveryPeriod']
    # 询价日期
    item['createDate'] = eve_data['createDate']
    if redis_db.hexists(redis_data_dict,
                        str(item['orderTitle']) + ':' + str(item['minNakedPrice']) + '~' + str(item['maxNakedPrice'])):
        print('数据库中已经存在该数据,不做处理~~~')
    else:
        redis_db.hset(redis_data_dict,
                      str(item['orderTitle']) + ':' + str(item['minNakedPrice']) + '~' + str(item['maxNakedPrice']), 0)
        sql = 'insert into ods_hn_qiugou(orderTitle,minNakedPrice,maxNakedPrice,totalCount,deliveryPeriod,createDate)values (%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['orderTitle'], item['minNakedPrice'], item['maxNakedPrice'], item['totalCount'],
            item['deliveryPeriod'],
            item['createDate']))
        conn.commit()
conn.close()
