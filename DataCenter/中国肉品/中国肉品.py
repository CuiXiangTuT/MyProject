import random
import time

import requests
from get_proxies import get_ip_list


def get_detail_data(id_list):
    # print(id_list)
    for per_id in id_list:
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
        json_data = {
            "id": per_id["id"]
        }
        item = dict()
        ip = random.choice(ip_list)
        res = requests.post(url=url, headers=headers, json=json_data,
                            proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["data"]
        # 产品名
        item["product"] = res["name"]
        # 价格
        item["price"] = res["price"]
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
        print(item)
        time.sleep(1)


def get_list_data():
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
    data_list = []
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
        data_list += id_list
    get_detail_data(data_list)


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_list_data()
