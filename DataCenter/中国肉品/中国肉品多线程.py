import datetime
import random
import threading
import time
from queue import Queue
import requests
from threading import Thread
from get_proxies import get_ip_list
import pymysql
import redis
import re


def insert_mysql(queue_into_mysql):
    item = queue_into_mysql.get()
    # 链接MySQL数据库
    conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc", port=3306)
    cursor = conn.cursor()
    # 链接Redis数据库
    redisDB = redis.Redis(host='127.0.0.1', port=6379, db=4)
    redis_dict_key = 'ods_china_meat'
    if redisDB.hexists(redis_dict_key,
                       item['product'] + "-" + str(item["price"]) + "-" +
                       item["contact_person"]):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key,
                     item['product'] + "-" + str(item["price"]) + "-" +
                     item["contact_person"], 0)
        sql = 'insert into ods_china_meat(product,price,factory_no,unit,validity_time,start_purchase,warehouse,stock,country,contact_person,phone,status,create_date,data_source,insert_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["product"], item["price"], item["factory_no"], item["unit"], item["validity_time"],
            item["start_purchase"],
            item["warehouse"],
            item["stock"], item["country"], item["contact_person"], item["phone"], item["status"], item["create_date"],
            item["data_source"], item["insert_time"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')
    conn.close()


def get_detail_data(queue_in, queue_out, save_mysql_queue):
    url = "http://app.meat.hongliaowang.com/meat/get"
    headers = {
        'authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMzUzYjA1MjA2MmMxMWVjOWI2MTAwMTYzZTM1ZmNhMyIsImlhdCI6MTYyOTk1NDY5MSwianRpIjoiIn0.Rqb9jRR-mmIiYz2WhcAnxafGVWAquWzWd8GyszmDKRE',
        'channel': '',
        'os': 'ANDROID',
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': '41',
        'Host': 'app.meat.hongliaowang.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.9.1',
    }
    while True:
        json_data = {
            "id": queue_in.get()
        }
        item = dict()
        ip = random.choice(ip_list)
        res = requests.post(url=url, headers=headers, json=json_data,
                            proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["data"]
        # 产品名
        item["product"] = res["name"]
        # 厂号
        item["factory_no"] = re.sub(re.compile(r'[\u4e00-\u9fa5]'), '', res["name"])
        # 价格
        item["price"] = str(res["price"])
        # 单位
        item["unit"] = res["unit"]
        # 有效期
        item["validity_time"] = str(res["validityTime"]) + "个月"
        # 起购
        item["start_purchase"] = str(res["leastCount"]) + res["unit"]
        # 仓库
        item["warehouse"] = res["stockAddress"]
        # 库存
        item["stock"] = str(res["stock"]) + res["unit"]
        # 产地
        item["country"] = res["madein"]
        # 联系人
        item["contact_person"] = res["linkman"]
        # 电话
        item["phone"] = res["tel"]
        # 供货类型
        item["status"] = "现货" if res["supplyType"] == 1 else "期货"
        # 创建时间
        item["create_date"] = res["createTime"]
        # 数据来源
        item["data_source"] = "中国肉品"
        # 插入时间
        item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%D %H:%M:%S")
        print(item)
        save_mysql_queue.put(item)
        queue_out.put(threading.current_thread().getName())


def get_list_data(queue_in):
    url = "http://app.meat.hongliaowang.com/meat/query"
    headers = {
        'channel': '',
        'os': 'ANDROID',
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': '96',
        'Host': 'app.meat.hongliaowang.com',
        # 'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.9.1',
    }
    for page_num in range(1, 3):
        json_data = {
            "category": "牛肉",
            "madein": "",
            "orderBy": "time",
            "pageIndex": page_num,
            "pageSize": 10,
            "stockAddress": ""
        }
        ip = random.choice(ip_list)
        id_list = requests.post(url=url, headers=headers, json=json_data,
                                proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["data"]["list"]
        for per_id in id_list:
            queue_in.put(per_id["id"])


if __name__ == '__main__':
    ip_list = get_ip_list()
    start_time = time.time()
    queue = Queue(maxsize=10)  # 设置队列最大空间为10
    result_queue = Queue()
    save_mysql_queue = Queue()
    print("queue开始大小为%d" % queue.qsize())

    get_list_data_thread = Thread(target=get_list_data, args=(queue,))
    get_list_data_thread.daemon = True
    get_list_data_thread.start()

    for index in range(10):
        get_detail_data_thread = Thread(target=get_detail_data, args=(queue, result_queue, save_mysql_queue,))
        get_detail_data_thread.daemon = True
        get_detail_data_thread.start()

    for index in range(10):
        insert_into_mysql_thread = Thread(target=insert_mysql, args=(save_mysql_queue,))
        insert_into_mysql_thread.daemon = True
        insert_into_mysql_thread.start()
    queue.join()
    end_time = time.time()

    print("总耗时：%s" % (end_time - start_time))
    print("queue 结束大小：%d" % queue.qsize())
    print("result_queue 结束大小：%d" % result_queue.qsize())
