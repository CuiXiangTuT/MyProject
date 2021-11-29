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
redis_dict_key = 'ods_bifu_zhunRuGuoNiuRouShuHuaData'


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
    if redisDB.hexists(redis_dict_key, item['publishTime'] + '-' + str(item['Brazil']) + '-' + str(item['Argentina'])+'-'+str(item['Type_C'])+'-'+str(item['Storage'])):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key, item['publishTime'] + '-' + str(item['Brazil']) + '-' + str(item['Argentina'])+'-'+str(item['Type_C'])+'-'+str(item['Storage']), 0)
        sql = 'insert into ods_bifu_zhunruguoniuroushuhuadata(Brazil,Argentina,Uruguay,Australia,NewZealand,USA,Canada,publishTime,Type_C,Storage,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['Brazil'], item['Argentina'], item['Uruguay'], item['Australia'], item['NewZealand'], item['USA'],
            item['Canada'], item['publishTime'],item['Type_C'],item['Storage'], item['insertTime']))
        conn.commit()
        print('该数据正在插入，稍等~~~')



# 获取数据
def getData():
    originList = ["巴西|阿根廷|乌拉圭|澳大利亚|新西兰", "美国|加拿大"]
    dateList = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09',
                '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
                '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03',
                '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
                '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08']
    df1 = pd.DataFrame(columns=['巴西', '阿根廷', '乌拉圭', '澳大利亚', '新西兰'], index=dateList)
    df2 = pd.DataFrame(columns=['美国', '加拿大'], index=dateList)
    for originIndex in range(len(originList)):
        url = 'https://www.beeftochina.com.cn/api/SystemApi/GetBeefWebDataOneChart'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
        }
        jsonData = {"MessageID": "7c05e3ce-c52f-45d5-b3fd-04683d61e17b", "MessageType": 2000000001,
                    "Data": {"UserID": "danaodaiyangyang", "LanguageCode": "zh-CN", "IsFirst": False,
                             "Origin": originList[originIndex], "Type": "总计", "Storage": "总计", "isEn": False}}
        ip = random.choice(ipList)
        response = requests.post(url=url, headers=headers, json=jsonData,
                                 proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['Data']['Row']
        series = response['series']
        if originIndex == 0:
            df1['巴西'] = series[0]['data']
            df1['阿根廷'] = series[1]['data']
            df1['乌拉圭'] = series[2]['data']
            df1['澳大利亚'] = series[3]['data']
            df1['新西兰'] = series[4]['data']
        else:
            df2['美国'] = series[0]['data'] + ['NaN']
            df2['加拿大'] = series[1]['data'] + ['NaN']
    df = pd.concat([df1, df2], axis=1)
    for perDate in dateList:
        # 巴西
        item['Brazil'] = '' if df.loc[perDate]['巴西'] == 'NaN' else df.loc[perDate]['巴西']
        item['Argentina'] = '' if df.loc[perDate]['阿根廷'] == 'NaN' else df.loc[perDate]['阿根廷']
        item['Uruguay'] = '' if df.loc[perDate]['乌拉圭'] == 'NaN' else df.loc[perDate]['乌拉圭']
        item['Australia'] = '' if df.loc[perDate]['澳大利亚'] == 'NaN' else df.loc[perDate]['澳大利亚']
        item['NewZealand'] = '' if df.loc[perDate]['新西兰'] == 'NaN' else df.loc[perDate]['新西兰']
        item['USA'] = '' if df.loc[perDate]['美国'] == 'NaN' else df.loc[perDate]['美国']
        item['Canada'] = '' if df.loc[perDate]['加拿大'] == 'NaN' else df.loc[perDate]['加拿大']
        item['publishTime'] = perDate
        item['Type_C'] = '总计'
        item['Storage'] = '总计'
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insertMysql(item)


if __name__ == '__main__':
    item = {}
    ipList = getIp()
    getData()
    cursor.close()
    conn.close()
