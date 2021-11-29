import datetime
import random

from get_proxies import get_ip_list
import pymysql
import redis
import requests

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=4)
redis_dict_key = 'ods_bifu_india_import_volumn'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key,
                       item['destination_country'] + "-" + item["import_volume"] + "-" +
                       item["start_date"]):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key,
                     item['destination_country'] + "-" + item["import_volume"] + "-" +
                     item["start_date"], 0)
        sql = 'insert into ods_bifu_india_import_volumn(trading_country,start_date,end_date,destination_country,import_volume,unit,insert_time,data_source)values (%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["trading_country"], item["start_date"], item["end_date"], item["destination_country"],
            item["import_volume"],
            item["unit"],
            item["insert_time"], item["data_source"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_list_date():
    url = "https://www.beeftochina.com.cn/api/SystemApi/GetBeefWebDataTwoTable"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
    }
    date_list = [201901, 201902, 201903, 201904, 201905, 201906, 201907, 201908, 201909, 201910, 201911, 201912, 202001,
                 202002, 202003, 202004, 202005, 202006, 202007, 202008, 202009, 202010, 202011, 202012, 202101, 202102,
                 202103, 202104, 202105, 202106, 202107, 202108, 202109]
    for per_date in date_list:
        item = dict()
        json_data = {"MessageID": "6bf48e14-09b4-4334-bad0-ecf6de2d764c", "MessageType": 2000000004,
                     "Data": {"UserID": "danaodaiyangyang", "LanguageCode": "zh-CN", "IsFirst": False, "Origin": "印度",
                              "Type": "总计", "Storage": "总计", "Feeding": "总计", "StartDate": str(per_date),
                              "EndDate": str(per_date),
                              "isEn": False}}
        ip = random.choice(ip_list)
        res = requests.post(url=url, headers=headers, json=json_data,proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["Data"]["Row"]["tableData"][1:]
        item["start_date"] = str(per_date)
        item["end_date"] = str(per_date)
        item["unit"] = "吨"
        item["trading_country"] = "巴西"
        item["data_source"] = "BTC"
        for per_json in res:
            item["destination_country"] = per_json["Destination"]
            item["import_volume"] = per_json["Volume"]
            item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(item)
            insert_mysql(item)


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_list_date()
