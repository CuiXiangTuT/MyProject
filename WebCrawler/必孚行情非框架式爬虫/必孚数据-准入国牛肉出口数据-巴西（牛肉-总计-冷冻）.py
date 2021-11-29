import random
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
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_bifu_zhunRuGuoNiuRouChuKouData'


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
    if redisDB.hexists(redis_dict_key,
                       str(item['ChineseMainland']) + '-' + str(item['Chile']) + '-' + str(
                           item['HongKongChina']) + '-' + str(
                           item['TheUnitedArabEmirates']) + '-' + str(item['thePhilippines']) + '-' + str(
                           item['thePhilippines']) + '-' + str(item['Storage']) + '-' + str(
                           item['Feeding']) + '-' + str(item['USA'])+'-'+str(item['meatName'])):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key,
                     str(item['ChineseMainland'])+ '-' + str(item['Chile']) + '-' + str(item['HongKongChina']) + '-' + str(
                         item['TheUnitedArabEmirates']) + '-' + str(item['thePhilippines']) + '-' + str(
                         item['thePhilippines']) + '-' + str(item['Storage']) + '-' + str(
                         item['Feeding']) + '-' + str(item['USA'])+'-'+str(item['meatName']), 0)
        sql = 'insert into ods_bifu_zhunruguoniurouchukoudata(totalCount,ChineseMainland,Chile,HongKongChina,Egypt,USA,SaudiArabia,Israel,TheUnitedArabEmirates,thePhilippines,publishTime,Type_C,Storage,Feeding,origin,meatName,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['totalCount'], item['ChineseMainland'], item['Chile'], item['HongKongChina'], item['Egypt'],
            item['USA'], item['SaudiArabia'], item['Israel'], item['TheUnitedArabEmirates'], item['thePhilippines'],
            item['publishTime'], item['Type_C'], item['Storage'], item['Feeding'], item['origin'],item['meatName'], item['insertTime']))
        conn.commit()
        print('该数据正在插入，稍等~~~')


# 获取数据
def getData():
    originList = ["总计|中国大陆|智利|中国香港|埃及", "美国|沙特阿拉伯|以色列|阿联酋|菲律宾"]
    dateList = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09',
                '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
                '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03',
                '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
                '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08']
    df1 = pd.DataFrame(columns=['总计', '中国大陆', '智利', '中国香港', '埃及'], index=dateList)
    df2 = pd.DataFrame(columns=['美国', '沙特阿拉伯', '以色列', '阿联酋', '菲律宾'], index=dateList)
    for originIndex in range(len(originList)):
        url = 'https://www.beeftochina.com.cn/api/SystemApi/GetBeefWebDataTwoChart'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
        }
        jsonData = {"MessageID": "e3a40906-7205-4d56-9b25-af4160c304d4", "MessageType": 2000000003,
                    "Data": {"UserID": "danaodaiyangyang", "LanguageCode": "zh-CN", "IsFirst": False, "Origin": "巴西",
                             "Destination": originList[originIndex], "Type": "总计", "Storage": "总计", "Feeding": "总计",
                             "isEn": False}}
        # ip = random.choice(ipList)
        response = requests.post(url=url, headers=headers, json=jsonData).json()['Data']['Row']
        series = response['series']
        if originIndex == 0:
            df1['总计'] = series[0]['data']
            df1['中国大陆'] = series[1]['data']
            df1['智利'] = series[2]['data']
            df1['中国香港'] = series[3]['data']
            df1['埃及'] = series[4]['data']
        else:
            df2['美国'] = series[0]['data']
            df2['沙特阿拉伯'] = series[1]['data']
            df2['以色列'] = series[2]['data']
            df2['阿联酋'] = series[3]['data']
            df2['菲律宾'] = series[4]['data']
    df = pd.concat([df1, df2], axis=1)
    for perDate in dateList:
        # 巴西
        item['totalCount'] = '' if df.loc[perDate]['总计'] == 'NaN' else df.loc[perDate]['总计']
        item['ChineseMainland'] = '' if df.loc[perDate]['中国大陆'] == 'NaN' else df.loc[perDate]['中国大陆']
        item['Chile'] = '' if df.loc[perDate]['智利'] == 'NaN' else df.loc[perDate]['智利']
        item['HongKongChina'] = '' if df.loc[perDate]['中国香港'] == 'NaN' else df.loc[perDate]['中国香港']
        item['Egypt'] = '' if df.loc[perDate]['埃及'] == 'NaN' else df.loc[perDate]['埃及']
        item['USA'] = '' if df.loc[perDate]['美国'] == 'NaN' else df.loc[perDate]['美国']
        item['SaudiArabia'] = '' if df.loc[perDate]['沙特阿拉伯'] == 'NaN' else df.loc[perDate]['沙特阿拉伯']
        item['Israel'] = '' if df.loc[perDate]['以色列'] == 'NaN' else df.loc[perDate]['以色列']
        item['TheUnitedArabEmirates'] = '' if df.loc[perDate]['阿联酋'] == 'NaN' else df.loc[perDate]['阿联酋']
        item['thePhilippines'] = '' if df.loc[perDate]['菲律宾'] == 'NaN' else df.loc[perDate]['菲律宾']
        item['publishTime'] = perDate
        item['Type_C'] = '总计'
        item['Storage'] = '总计'
        item['Feeding'] = '总计'
        item['origin'] = '巴西'
        item['meatName'] = '牛肉'
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # insertMysql(item)
        print(item)


if __name__ == '__main__':
    item = {}
    # ipList = getIp()
    getData()
    cursor.close()
    conn.close()
