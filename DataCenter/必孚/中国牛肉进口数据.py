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
redis_dict_key = 'ods_bifu_import_volumn'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key,
                       item['is_there_bone'] + '-' + str(item['storage_mode']) + "-" + item["import_volume"] + "-" +
                       item["start_date"] + "-" + item["country"]):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key,
                     item['is_there_bone'] + '-' + str(item['storage_mode']) + "-" + item["import_volume"] + "-" +
                     item["start_date"] + "-" + item["country"], 0)
        sql = 'insert into ods_bifu_import_volumn(is_there_bone,storage_mode,country,import_volume,unit,start_date,end_date,insert_time,data_source)values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["is_there_bone"], item["storage_mode"], item["country"], item["import_volume"], item["unit"],
            item["start_date"],
            item["end_date"], item["insert_time"],
            item["data_source"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_list_data():
    url = "https://www.beeftochina.com.cn/api/SystemApi/GetBeefWebDataSixTable"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
    }
    date_list = [201901, 201902, 201903, 201904, 201905, 201906, 201907, 201908, 201909, 201910, 201911, 201912, 202001,
                 202002, 202003, 202004, 202005, 202006, 202007, 202008, 202009, 202010, 202011, 202012, 202101, 202102,
                 202103, 202104, 202105, 202106, 202107, 202108, 202109]
    for per_date in date_list:
        for front_sort in ["带骨", "去骨"]:
            for back_sort in ["冷冻", "冰鲜"]:
                item = dict()
                json_data = {"MessageID": "b1cfd0ba-ad17-41a8-a3b0-681b11996a1a", "MessageType": 2000000012,
                             "Data": {"isEn": False, "UserID": "danaodaiyangyang", "LanguageCode": "zh-CN",
                                      "IsFirst": False,
                                      "Type": front_sort, "Storage": back_sort, "StartDate": str(per_date),
                                      "EndDate": str(per_date)}}
                ip = random.choice(ip_list)
                res = requests.post(url=url, headers=headers, json=json_data,
                                    proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["Data"]["Row"][
                          "tableData"][1:]
                item["start_date"] = str(per_date)
                item["end_date"] = str(per_date)
                item["is_there_bone"] = front_sort
                item["storage_mode"] = back_sort
                item["data_source"] = "BTC"
                item["unit"] = "吨"
                for per_json in res:
                    item["country"] = per_json["Origin"]
                    item["import_volume"] = per_json["Volume"]
                    item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(item)
                    insert_mysql(item)


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_list_data()
