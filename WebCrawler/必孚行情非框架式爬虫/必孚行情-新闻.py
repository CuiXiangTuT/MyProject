from datetime import datetime

import pymysql
import redis
import requests

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redis_db = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_data_dict = 'ods_bifu_hangqingNews'


def insertMysql(item):
    if redis_db.hexists(redis_data_dict,item['title']+'-'+item['publishTime']):
        print('该数据已存在，不做处理...')
    else:
        redis_db.hset(redis_data_dict,item['title']+'-'+item['publishTime'],0)
        sql = 'insert into ods_bifu_hangqingnews(publishYear,title,newsContext,publishTime,insertTime)values (%s,%s,%s,%s,%s)'
        cursor.execute(sql,(item['publishYear'],item['title'],item['newsContext'],item['publishTime'],item['insertTime']))
        conn.commit()
        print('该数据正在插入，请稍等...')


def getData():
    yearList = ['2021','2020','2019']
    pageSize = [36,50,49]
    zipList = list(zip(yearList,pageSize))
    for perZip in zipList:
        url = 'https://www.beeftochina.com.cn/api/SystemApi/GetWebNewsAnalysis'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
        }
        jsonData = {"MessageID": "87db4364-1ce6-4e66-b273-00c9175c00c0", "MessageType": 3000000007,
                    "Data": {"PageNum": 1, "PageSize": perZip[1], "Year": perZip[0], "UserID": "danaodaiyangyang"}}
        # 年份
        item['publishYear'] = perZip[0]
        newsList = requests.post(url=url,headers=headers,json=jsonData).json()['Data']['Rows']
        for perNews in newsList:
            # 标题
            item['title'] = perNews['NewsTitle']
            # 内容
            item['newsContext'] = perNews['NewsContext'].replace('#',' ').replace('【来源：BTC必孚(中国)】','')
            # 发布时间
            item['publishTime'] = perNews['NewsDateTime']
            # 插入时间
            item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insertMysql(item)

if __name__ == '__main__':
    item = {}
    getData()
    cursor.close()
    conn.close()