import datetime
import random
from pprint import pprint

import pymysql
import redis
import requests
from get_proxies import get_ip_list

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=4)
redis_dict_key = 'ods_zhaoniuwang_agent_purchasing'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, item['product'] + "-" + item["price"] + "-" + item["create_date"]):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key, item['product'] + "-" + item["price"] + "-" + item["create_date"], 0)
        sql = 'insert into ods_zhaoniuwang_agent_purchasing(product,price,price_unit,stock,stock_unit,remark,overseas_remark,origin,provide_type,invoice_type,shipping_method,deposit,country_id,country,factory_no,cate_name,fat_to_thin_ratio,contact_person,phone,trader_name,trader_phone,create_date,data_source,insert_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, ((
            item["product"], item["price"], item["price_unit"], item["stock"], item["stock_unit"], item["remark"],
            item["overseas_remark"], item["origin"], item["provide_type"], item["invoice_type"],
            item["shipping_method"],
            item["deposit"], item["country_id"], item["country"], item["factory_no"], item["cate_name"],
            item["fat_to_thin_ratio"], item["contact_person"], item["phone"], item["trader_name"], item["trader_phone"],
            item["create_date"],
            item["data_source"], item["insert_time"])))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_detail_data(pid):
    url = "https://api.zhaoniuw.com/client/provideInfo/detail/{}".format(pid)
    headers = {
        'Host': 'api.zhaoniuw.com',
        'Accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VySWQiOiIzMGFkZGRmYzFiMjI0OTI0YmMwMjlhZDVkMTA3MjUwNyIsImV4cCI6MTcyNDIyOTg5MywibmJmIjoxNjM3ODI5ODkzfQ.cGYg6QkqHOPppgV4dwGtZ1ZRtrqeIV4bQSjB6OTUDDs',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; LIO-AN00 Build/LIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/24.0)',
        'X-Requested-With': 'com.zhaoniuw.app',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    ip = random.choice(ip_list)
    response = requests.get(url=url, headers=headers, proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()[
        "data"]
    item = dict()
    # 1.产品名
    item["product"] = response["title"]
    # 2.价格
    item["price"] = str(float(response["price"]) * 1000)
    # 3.价格单位
    item["price_unit"] = "美元/吨"
    # 4.代采数量
    item["stock"] = response["amount"]
    # 5.代采数量单位
    item["stock_unit"] = "吨"
    # 6.备注
    item["remark"] = response["remark"]
    # 7.国外备注
    item["overseas_remark"] = response["overseasRemark"]
    # 8.来源
    item["origin"] = response["source"] if response["source"] else ""
    # 9.期货/现货
    if response["provideWayId"] == 1:
        item["provide_type"] = "期货"
    elif response["provideWayId"] == 2:
        item["provide_type"] = "现货"
    else:
        item["provide_type"] = "不限"
    # 10.发票详情：带发票/不带发票
    if response["invoiceType"] == 1:
        item["invoice_type"] = "带发票"
    elif response["invoiceType"] == 2:
        item["invoice_type"] = "不带发票"
    else:
        item["invoice_type"] = "不限"
    # 11.出货方式
    if response["sellType"] == 0:
        item["shipping_method"] = "可散出"
    elif response["sellType"] == 1:
        item["shipping_method"] = "整出"
    else:
        item["shipping_method"] = ""
    # 12.定金
    item["deposit"] = str(response["deposit"]) + "%"
    # 13.产地国家ID
    item["country_id"] = response["countryId"]
    # 14.产地
    item["country"] = response["countryName"]
    # 15.厂号
    item["factory_no"] = response["factoryNo"]
    # 16.品名
    item["cate_name"] = response["cateName"]
    # 17.肥瘦比例
    item["fat_to_thin_ratio"] = str(response["scale"])
    # 18.联系人
    item["contact_person"] = response["userName"]
    # 19.联系人电话
    item["phone"] = response["userPhone"]
    # 20.交易员
    item["trader_name"] = response["trader_name"]
    # 21.交易员电话
    item["trader_phone"] = response["trader_phone"]
    # 22.发布时间
    item["create_date"] = ("2021/" + response["updateDate"]).replace("/", "-") + ":00"
    # 23.数据来源
    item["data_source"] = "找牛网"
    # 24.插入时间
    item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(item)
    # insert_mysql(item)


def get_list_data():
    url = "https://api.zhaoniuw.com/client/good/queryList"
    headers = {
        'Host': 'api.zhaoniuw.com',
        'Content-Length': '98',
        'Accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VySWQiOiIzMGFkZGRmYzFiMjI0OTI0YmMwMjlhZDVkMTA3MjUwNyIsImV4cCI6MTcyNDIyOTg5MywibmJmIjoxNjM3ODI5ODkzfQ.cGYg6QkqHOPppgV4dwGtZ1ZRtrqeIV4bQSjB6OTUDDs',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; LIO-AN00 Build/LIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36 Html5Plus/1.0 (Immersed/24.0)',
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Requested-With': 'com.zhaoniuw.app',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    for page_num in range(1, 6):
        json_data = {
            "uuid": "30adddfc1b224924bc029ad5d1072507",
            "pageNumber": page_num,
            "pageSize": 20,
            "goodType": 2,
            "overseas": 1
        }
        ip = random.choice(ip_list)
        response = requests.post(url=url, headers=headers, json=json_data,
                                 proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["data"]["list"]
        for per_id in response:
            get_detail_data(per_id["id"])


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_list_data()
    cursor.close()
    conn.close()
