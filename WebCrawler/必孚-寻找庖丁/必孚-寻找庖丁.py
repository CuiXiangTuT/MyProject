from datetime import datetime

import pymysql
import redis
import requests


# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'bifuxunzhaopaoding'

# 入库
def insertMysql(item):
    if redisDB.hexists(redis_dict_key,item['origin']+item['company']+item['estNo']):
        print('数据已存在，')
    else:
        redisDB.hset(redis_dict_key,item['origin']+item['company']+item['estNo'],0)
        sql = 'insert into ods_bifuxunzhaopaoding(origin,originEn,orderRank,estNum,companyNum,company,CestNum,estNo,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,(item['origin'],item['originEn'],item['orderRank'],item['estNum'],item['companyNum'],item['company'],item['CestNum'],item['estNo'],item['insertTime']))
        conn.commit()


def GetBeefCutsResearchEst(origin, company):
    url = 'http://47.96.113.183:8080/api/SystemApi/GetBeefCutsResearchEst'
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.0)",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "126",
        "Host": "47.96.113.183:8080",
        # "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    jsonData = {
        "MessageType": 70006,
        "MessageID": "a7d131d1-0fef-45ca-88c9-ba081fb171a6",
        "Data": {
            "Origin": origin,
            "Company": company,
            "EstNo": ""
        }
    }
    responseList = requests.post(url=url, headers=headers, json=jsonData).json()['Data']['Datas']['Items']
    for everyData in responseList:
        # 厂号
        item['estNo'] = everyData['EstNo']
        # 插入时间
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(item)
        insertMysql(item)


def getBeefCutsResearchCompany(origin):
    url = 'http://47.96.113.183:8080/api/SystemApi/GetBeefCutsResearchCompany'
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.0)",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "112",
        "Host": "47.96.113.183:8080",
        # "Connection":"Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    jsonData = {
        "MessageType": 70005,
        "MessageID": "3f890e00-c38d-4b6a-ba76-dc019513431b",
        "Data": {
            "Origin": origin,
            "Company": ""
        }
    }
    responseList = requests.post(url=url, headers=headers, json=jsonData).json()['Data']['Datas']['Items']
    for everyData in responseList:
        # 公司名
        item['company'] = everyData['Company']
        # 该公司输华工厂数量
        item['CestNum'] = everyData['EstNum']
        GetBeefCutsResearchEst(origin, everyData['Company'])


def getBeefCutsRearchEst():
    url = 'http://47.96.113.183:8080/api/SystemApi/GetBeefCutsResearchOrigin'
    headers = {
        "user-agent": "Mozilla/5.0 (Linux; Android 7.1.2; SM-G977N Build/LMY48Z; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.143 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/24.0)",
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": "93",
        "Host": "47.96.113.183:8080",
        # "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    jsonData = {
        "MessageType": 70004,
        "MessageID": "8b5df718-e676-4d59-9874-4fd699b34346",
        "Data": {
            "Origin": ""
        }
    }
    responseList = requests.post(url=url, headers=headers, json=jsonData).json()["Data"]["Datas"]["Items"]
    for everyData in responseList:
        # 起源（中文）
        item['origin'] = everyData['Origin']
        # 起源（英文）
        item['originEn'] = everyData['OriginEn']
        # 输华体量排名
        item['orderRank'] = everyData['Order']
        # 输华工厂数量
        item['estNum'] = everyData['EstNum']
        # 公司数量
        item['companyNum'] = everyData['CompanyNum']
        getBeefCutsResearchCompany(everyData['Origin'])


if __name__ == '__main__':
    item = {}
    getBeefCutsRearchEst()
    cursor.close()
    conn.close()

