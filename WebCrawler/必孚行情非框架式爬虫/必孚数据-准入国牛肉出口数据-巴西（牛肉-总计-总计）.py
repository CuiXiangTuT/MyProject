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
    originList = ['总计|中国大陆|中国香港|埃及|智利', '阿联酋|伊朗|沙特阿拉伯|菲律宾|俄罗斯', '意大利|以色列|乌拉圭|新加坡|约旦', '荷兰|土耳其|美国|黎巴嫩|阿尔及利亚', '阿根廷|利比亚|西班牙|巴勒斯坦|马来西亚', '德国|印度尼西亚|阿尔巴尼亚|安哥拉|伊拉克', '格鲁吉亚|英国|塞尔维亚|卡塔尔|巴拉圭', '秘鲁|加蓬|其他|尼日尔|瑞典', '泰国|越南|瑞士|阿鲁巴|突尼斯', '库拉索|阿曼|南非|巴林|马其顿', '葡萄牙|澳大利亚|科特迪瓦|韩国|亚美尼亚', '科威特|古巴|加拿大|巴哈马|利比里亚', '科摩罗|波多黎各|土库曼斯坦|比利时|百慕大群岛', '希腊|塞舌尔|毛里求斯|缅甸|佛得角', '阿塞拜疆|马尔代夫|摩洛哥|加纳|塞内加尔', '刚果（金）|丹麦|芬兰|法国|刚果（布）', '赤道几内亚|玻利维亚|巴拿马|马绍尔群岛|挪威', '中非共和国|圣马丁岛|格林纳达|黑山|爱尔兰', '文莱|马耳他|坦桑尼亚|安提瓜和巴布达|塔吉克斯坦', '纳米比亚|中国澳门|加那利群岛|塞浦路斯|印度', '荷属安的列斯群岛|乌克兰|多米尼加|老挝|吉布提', '洪都拉斯|几内亚|波内赫、圣尤斯特歇斯和萨巴|莫桑比克|格拉纳达', '所罗门群岛|海地|毛里塔尼亚|苏里南|中国台湾', '哈萨克斯坦|留尼汪岛|科麦隆|阿富汗|摩纳哥', '斯里兰卡|日本|塞拉利昂|马里|英属维尔京群岛', '开曼群岛|圣多美与普林希比|马恩岛|冰岛|巴巴多斯', '圭亚那|伯利兹|直布罗陀|圣维森特和格拉纳丁斯|波黑', '拉脱维亚|克罗地亚|巴西|图瓦卢|哥伦比亚', '保加利亚|巴基斯坦|卢森堡|波兰|福克兰群岛', '斯威士兰|罗马尼亚|斯洛伐克|孟加拉国|马达加斯加', '朝鲜|瓦努阿图|基里巴斯|蒙古国|泽西岛']
    dateList = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09',
                '2018-10', '2018-11', '2018-12', '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06',
                '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12', '2020-01', '2020-02', '2020-03',
                '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
                '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08']
    l = ['总计', '中国大陆', '中国香港', '埃及', '智利', '阿联酋', '伊朗', '沙特阿拉伯', '菲律宾', '俄罗斯', '意大利', '以色列', '乌拉圭', '新加坡', '约旦', '荷兰',
         '土耳其', '美国', '黎巴嫩', '阿尔及利亚', '阿根廷', '利比亚', '西班牙', '巴勒斯坦', '马来西亚', '德国', '印度尼西亚', '阿尔巴尼亚', '安哥拉', '伊拉克', '格鲁吉亚',
         '英国', '塞尔维亚', '卡塔尔', '巴拉圭', '秘鲁', '加蓬', '其他', '尼日尔', '瑞典', '泰国', '越南', '瑞士', '阿鲁巴', '突尼斯', '库拉索', '阿曼', '南非',
         '巴林', '马其顿', '葡萄牙', '澳大利亚', '科特迪瓦', '韩国', '亚美尼亚', '科威特', '古巴', '加拿大', '巴哈马', '利比里亚', '科摩罗', '波多黎各', '土库曼斯坦',
         '比利时', '百慕大群岛', '希腊', '塞舌尔', '毛里求斯', '缅甸', '佛得角', '阿塞拜疆', '马尔代夫', '摩洛哥', '加纳', '塞内加尔', '刚果（金）', '丹麦', '芬兰',
         '法国', '刚果（布）', '赤道几内亚', '玻利维亚', '巴拿马', '马绍尔群岛', '挪威', '中非共和国', '圣马丁岛', '格林纳达', '黑山', '爱尔兰', '文莱', '马耳他',
         '坦桑尼亚', '安提瓜和巴布达', '塔吉克斯坦', '纳米比亚', '中国澳门', '加那利群岛', '塞浦路斯', '印度', '荷属安的列斯群岛', '乌克兰', '多米尼加', '老挝', '吉布提',
         '洪都拉斯', '几内亚', '波内赫、圣尤斯特歇斯和萨巴', '莫桑比克', '格拉纳达', '所罗门群岛', '海地', '毛里塔尼亚', '苏里南', '中国台湾', '哈萨克斯坦', '留尼汪岛', '科麦隆',
         '阿富汗', '摩纳哥', '斯里兰卡', '日本', '塞拉利昂', '马里', '英属维尔京群岛', '开曼群岛', '圣多美与普林希比', '马恩岛', '冰岛', '巴巴多斯', '圭亚那', '伯利兹',
         '直布罗陀', '圣维森特和格拉纳丁斯', '波黑', '拉脱维亚', '克罗地亚', '巴西', '图瓦卢', '哥伦比亚', '保加利亚', '巴基斯坦', '卢森堡', '波兰', '福克兰群岛', '斯威士兰',
         '罗马尼亚', '斯洛伐克', '孟加拉国', '马达加斯加', '朝鲜', '瓦努阿图', '基里巴斯', '蒙古国', '泽西岛']

    df = pd.DataFrame(columns=l, index=dateList)
    for originIndex in range(len(originList)):
        url = 'https://www.beeftochina.com.cn/api/SystemApi/GetBeefWebDataTwoChart'
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
        }
        jsonData = {"MessageID": "e3a40906-7205-4d56-9b25-af4160c304d4", "MessageType": 2000000003,
                    "Data": {"UserID": "danaodaiyangyang", "LanguageCode": "zh-CN", "IsFirst": False, "Origin": "巴西",
                             "Destination": originList[originIndex], "Type": "总计", "Storage": "总计", "Feeding": "总计",
                             "isEn": False}}

        response = requests.post(url=url, headers=headers, json=jsonData,).json()['Data']['Row']['series']

        # ip = random.choice(ipList)
        # response = requests.post(url=url, headers=headers, json=jsonData,
        #                          proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['Data']['Row']['series']
        wordList = originList[originIndex].split('|')
        # df[wordList[0]] = response[0]['data']
        # df[wordList[0]] = df[wordList[0]].replace(np.nan,' ')
        # df[wordList[1]] = response[1]['data']
        # df[wordList[1]] = df[wordList[1]].replace(np.nan,' ')
        # df[wordList[2]] = response[2]['data']
        # df[wordList[2]] = df[wordList[2]].replace(np.nan,' ')
        # df[wordList[3]] = response[3]['data']
        # df[wordList[3]] = df[wordList[3]].replace(np.nan,' ')
        # df[wordList[4]] = response[4]['data']
        # df[wordList[4]] = df[wordList[4]].replace(np.nan,' ')
        print(df)
    # for perDate in dateList:
    #     # 巴西
    #     item['totalCount'] = '' if df.loc[perDate]['总计'] == 'NaN' else df.loc[perDate]['总计']
    #     item['ChineseMainland'] = '' if df.loc[perDate]['中国大陆'] == 'NaN' else df.loc[perDate]['中国大陆']
    #     item['Chile'] = '' if df.loc[perDate]['智利'] == 'NaN' else df.loc[perDate]['智利']
    #     item['HongKongChina'] = '' if df.loc[perDate]['中国香港'] == 'NaN' else df.loc[perDate]['中国香港']
    #     item['Egypt'] = '' if df.loc[perDate]['埃及'] == 'NaN' else df.loc[perDate]['埃及']
    #     item['USA'] = '' if df.loc[perDate]['美国'] == 'NaN' else df.loc[perDate]['美国']
    #     item['SaudiArabia'] = '' if df.loc[perDate]['沙特阿拉伯'] == 'NaN' else df.loc[perDate]['沙特阿拉伯']
    #     item['Israel'] = '' if df.loc[perDate]['以色列'] == 'NaN' else df.loc[perDate]['以色列']
    #     item['TheUnitedArabEmirates'] = '' if df.loc[perDate]['阿联酋'] == 'NaN' else df.loc[perDate]['阿联酋']
    #     item['thePhilippines'] = '' if df.loc[perDate]['菲律宾'] == 'NaN' else df.loc[perDate]['菲律宾']
    #     item['publishTime'] = perDate
    #     item['Type_C'] = '总计'
    #     item['Storage'] = '总计'
    #     item['Feeding'] = '总计'
    #     item['origin'] = '巴西'
    #     item['meatName'] = '牛肉'
    #     item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     insertMysql(item)
    #     print(item)


if __name__ == '__main__':
    item = {}
    # ipList = getIp()
    getData()
    cursor.close()
    conn.close()
