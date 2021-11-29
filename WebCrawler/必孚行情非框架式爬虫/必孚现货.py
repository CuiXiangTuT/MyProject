import datetime
import json
import random
import uuid
import redis
import pymysql
import requests

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redis_db = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_data_dict = 'bifuhangqing'


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


# 获取日期ReportIDList
def getReportListFunc():
    url = 'https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceVaildDate'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
        'referer': 'https://www.beeftochina.com.cn/cn/BTCPrice',
        'content-type': 'application/json;charset=UTF-8'
    }
    data = {"MessageID": "8e11e168-1de8-4d58-9c17-7c062d124484", "MessageType": 3000000003,
            "Data": {"ReportType": "_spotgoods", "LanguageCode": "zh-CN"}}
    randomIp = random.choice(ipList)
    dataJsonList = requests.post(url=url, headers=headers, data=json.dumps(data),
                                 proxies={"http": 'http://' + str(randomIp['ip']) + ':' + randomIp['port']}).json()['Data']['List']
    reportIDList = []
    for everyData in dataJsonList:
        reportIDList.append(everyData['ReportID'])
    return reportIDList


def insertMysql(item):
    if redis_db.hexists(redis_data_dict,
                        str(item['beefPriceDataID']) + '-' + str(item['createDate']) + '-' + str(
                            item['feedingMode']) + '-' + str(item['originPlace']) + '-' + str(
                            item['beefpart']) + '-' + str(item['preReferencePrice']) + '-' + str(
                            item['referencePrice']) + '-' + str(item['maxReferencePrice']) + '-' + str(
                            item['minReferencePrice']) + '-' + str(item['riseRate']) + '-' + str(
                            item['historicalDate']) + '-' + str(item['keyWords']) + '-' + str(
                            item['growthRate']) + '-' + str(item['atThatTimePrice'])):
        # 若存在，输出数据库已经存在该数据
        print('数据库中已经存在该数据,不做处理~~~')

    else:
        print('正在入库，请稍等~~~')
        # 若不存在，则将URL写入Redis数据库中
        # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
        redis_db.hset(redis_data_dict,
                      str(item['beefPriceDataID']) + '-' + str(item['createDate']) + '-' + str(
                          item['feedingMode']) + '-' + str(item['originPlace']) + '-' + str(
                          item['beefpart']) + '-' + str(item['preReferencePrice']) + '-' + str(
                          item['referencePrice']) + '-' + str(item['maxReferencePrice']) + '-' + str(
                          item['minReferencePrice']) + '-' + str(item['riseRate']) + '-' + str(
                          item['historicalDate']) + '-' + str(item['keyWords']) + '-' + str(
                          item['growthRate']) + '-' + str(item['atThatTimePrice']), 0)
        # 进行MySQL入库处理
        sql = 'insert into ods_bifuhangqing(beefPriceDataID,createDate,feedingMode,originPlace,beefpart,preReferencePrice,referencePrice,maxReferencePrice,minReferencePrice,riseRate,historicalDate,keyWords,growthRate,atThatTimePrice,goodsStatus,curTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['beefPriceDataID'], item['createDate'], item['feedingMode'], item['originPlace'], item['beefpart'],
            item['preReferencePrice'], item['referencePrice'], item['maxReferencePrice'], item['minReferencePrice'],
            item['riseRate'], item['historicalDate'], item['keyWords'], item['growthRate'], item['atThatTimePrice'],
            item['goodsStatus'],
            item['curTime']))
        conn.commit()


def getData():
    reportIDList = getReportListFunc()
    for feedName in ['草饲', '谷饲']:
        for reportIdIndex in range(len(reportIDList)):
            item = {}
            url = 'https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceDataList'
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                'content-type': 'application/json;charset=UTF-8',
                'referer': 'https://www.beeftochina.com.cn/cn/BTCPrice',
            }
            if reportIdIndex == len(reportIDList) - 1:
                data = {"MessageID": str(uuid.uuid4()), "MessageType": 3000000001,
                        "Data": {"UserID": "danaodaiyangyang", "ReportID": reportIDList[reportIdIndex],
                                 "PreReportID": reportIDList[reportIdIndex], "OriginPlace": "全部",
                                 "Part": "全部", "FeedingMode": feedName}}
            else:
                data = {"MessageID": str(uuid.uuid4()), "MessageType": 3000000001,
                        "Data": {"UserID": "danaodaiyangyang", "ReportID": reportIDList[reportIdIndex],
                                 "PreReportID": reportIDList[reportIdIndex + 1],
                                 "OriginPlace": "全部",
                                 "Part": "全部", "FeedingMode": feedName}}
            randomIp = random.choice(ipList)
            dataList = requests.post(url=url, headers=headers, data=json.dumps(data),
                                     proxies={"http": 'http://' + str(randomIp['ip']) + ':' + randomIp['port']}).json()[
                'Data'][
                'Rows']
            item['goodsStatus'] = '现货'
            for perData in dataList:
                # 牛肉价格数据id
                item['beefPriceDataID'] = perData['BeefPriceDataID']
                # 创建日期
                item['createDate'] = perData['CreateDate']
                # 草饲 谷饲
                item['feedingMode'] = perData['FeedingMode']
                # 产地
                item['originPlace'] = perData['OriginPlace']
                # 部位
                item['beefpart'] = perData['Part']
                # 预参考价格
                item['preReferencePrice'] = perData['PreReferencePrice']
                # 参考价格
                item['referencePrice'] = perData['ReferencePrice']
                # 最大参考价格
                item['maxReferencePrice'] = perData['MaxReferencePrice']
                # 最小参考价格
                item['minReferencePrice'] = perData['MinReferencePrice']
                # 上升率
                item['riseRate'] = perData['RiseRate']
                # 走势
                detailUrl = 'https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceDataIndex'
                detailHeaders = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
                    'content-type': 'application/json;charset=UTF-8',
                    'referer': 'https://www.beeftochina.com.cn/cn/BTCPrice',
                }
                detailData = {"MessageID": str(uuid.uuid4()), "MessageType": 3000000004,
                              "Data": {"UserID": "danaodaiyangyang", "Part": perData['Part'],
                                       "Country": perData['OriginPlace'],
                                       "RecommendDay": 0,
                                       "FeedingMode": perData['FeedingMode'], "Type": "_spotgoods", "IsFirst": True,
                                       "IsEn": False}}
                response1 = requests.post(url=detailUrl, headers=detailHeaders, data=json.dumps(detailData),
                                          proxies={"http": 'http://' + str(randomIp['ip']) + ':' + randomIp['port']})
                detailDataList = response1.json()['Data']['Row']
                # 抽出日期列表
                dateList = detailDataList['categories']
                # 抽出涨幅列表
                riseList = detailDataList['riseList'][0]
                # 抽出价格列表
                priceList = detailDataList['series'][0]['data']
                # 将三组数据进行打包处理
                zipData = zip(dateList, riseList, priceList)
                for perData in zipData:
                    # 历史日期
                    item['historicalDate'] = perData[0]
                    # 关键词
                    item['keyWords'] = perData[1]['key']
                    # 增长率
                    item['growthRate'] = perData[1]['rise']
                    # 当时价格
                    item['atThatTimePrice'] = perData[2]
                    # 插入时间
                    item['curTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(item)
                    insertMysql(item)


if __name__ == '__main__':
    ipList = getIp()
    getData()
    cursor.close()
    conn.close()
