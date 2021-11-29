import datetime
import random

import pymysql
import redis

from get_proxies import get_ip_list

import requests

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=4)
redis_dict_key = 'ods_btc_realtime_quotes_spot_goods'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, item['create_date'] + '-' + str(item['max_reference_price']) + '-' + str(
            item['min_reference_price']) + '-' + str(item['country']) + '-' + str(item['part']) + '-' + str(
        item['rise'])):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key, item['create_date'] + '-' + str(item['max_reference_price']) + '-' + str(
            item['min_reference_price']) + '-' + str(item['country']) + '-' + str(
            item['part']) + '-' + str(item['rise']), 0)
        sql = 'insert into ods_btc_quote_actual(create_date,feeding_mode,country,part,unit,grade,max_reference_price,min_reference_price,pre_reference_price,reference_price,rise,rise_rate,data_source,insert_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["create_date"], item["feeding_mode"],
            item["country"], item["part"], item["unit"], item["grade"], item["max_reference_price"],
            item["min_reference_price"], item["pre_reference_price"],
            item["reference_price"], item["rise"], item["rise_rate"], item["data_source"], item["insert_time"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_date_list():
    """
    获取日期列表
    :return:
    """
    url = "https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceVaildDate"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
    }
    json_data = {"MessageID": "eb2afd24-e465-4ae5-ba14-3ebe3cab8744", "MessageType": 3000000003,
                 "Data": {"ReportType": "_spotgoods", "LanguageCode": "zh-CN"}}
    ip = random.choice(ip_list)
    res = requests.post(url=url, headers=headers, json=json_data,
                        proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["Data"]["List"]
    date_list = []
    for per_json in res:
        date_list.append((per_json["ReportID"], per_json["ReportDateTime"]))

    return date_list


def get_list_data(date_list):
    """
    获取数据
    :param date_list:日期列表
    :return:
    """
    url = "https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceDataList"
    for feeding_mode in ["草饲", "谷饲"]:
        for date_index in range(len(date_list)):
            if date_index + 1 != len(date_list):
                item = dict()
                headers = {
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
                }
                json_data = {"MessageID": "d9a1c006-a088-4657-b253-44050ed83d64", "MessageType": 3000000001,
                             "Data": {"UserID": "danaodaiyangyang", "ReportID": date_list[date_index][0],
                                      "PreReportID": date_list[date_index + 1][0], "OriginPlace": "全部",
                                      "Part": "全部", "FeedingMode": feeding_mode}}
                ip = random.choice(ip_list)
                res = requests.post(url=url, headers=headers, json=json_data,
                                    proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["Data"][
                    "Rows"]
                try:
                    for per_json in res:
                        # 创建日期
                        item["create_date"] = date_list[date_index][1]
                        # 饲养方式
                        item["feeding_mode"] = per_json["FeedingMode"]
                        try:
                            # 最高参考价
                            item["max_reference_price"] = per_json["MaxReferencePrice"]
                        except:
                            item["max_reference_price"] = ""
                        try:
                            # 最高参考价
                            item["min_reference_price"] = per_json["MinReferencePrice"]
                        except:
                            item["min_reference_price"] = ""
                        # 国家
                        item["country"] = per_json["OriginPlace"]
                        # 部位
                        item["part"] = per_json["Part"]
                        # 单位
                        item["unit"] = "元/公斤"
                        # 等级
                        item["grade"] = per_json["Level"]
                        # 预参考价格
                        item["pre_reference_price"] = per_json["PreReferencePrice"]
                        # 参考价
                        item["reference_price"] = per_json["ReferencePrice"]
                        # 增长数
                        item["rise"] = per_json["Rise"]
                        # 增长率
                        item["rise_rate"] = per_json["RiseRate"]
                        # 数据来源
                        item["data_source"] = "BTC"
                        # 插入时间
                        item["insert_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(item)
                        insert_mysql(item)
                except:
                    pass


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_list_data(get_date_list())
