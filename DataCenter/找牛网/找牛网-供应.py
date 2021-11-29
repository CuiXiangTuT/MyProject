import datetime
import random
import requests
from get_proxies import get_ip_list
import pymysql
import redis

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=4)
redis_dict_key = 'ods_zhaoniuwang_supply'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, item['product'] + "-" + item["price"] + "-" + item["create_date"]):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key, item['product'] + "-" + item["price"] + "-" + item["create_date"], 0)
        sql = 'insert into ods_zhaoniuwang_supply(product,price,unit,stock,stock_unit,create_date,origin,remark,overseas_remark,provide_type,invoice_type,shipping_method,deposit,country_id,country,factory_no,cate_name,fat_to_thin_ratio,contact_person,phone,trader_name,trader_phone,data_type,data_source,insert_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["product"], item["price"], item["unit"], item["stock"],item["stock_unit"], item["create_date"], item["origin_of_place"],
            item["remark"], item["overseas_remark"], item["provide_type"], item["invoice_type"],
            item["shipping_method"],
            item["deposit"], item["country_id"], item["country"], item["factory_no"], item["cate_name"],
            item["fat_to_thin_ratio"], item["contact_person"], item["phone"], item["trader_name"], item["trader_phone"],
            item["data_type"], item["data_source"], item["insert_time"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_detail_data(pid):
    url = "https://api.zhaoniuw.com/client/provideInfo/detail/" + str(pid)
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
    # 3.单位
    item["unit"] = "元/吨"
    # 4.库存数量
    item["stock"] = response["amount"]
    # 4.1 库存单位
    item["stock_unit"] = "吨"
    # 5.创建时间
    item["create_date"] = response["updateDate"]
    # 6.货源地
    item["origin"] = response["source"]
    # 7.备注
    item["remark"] = response["remark"]
    # 8.国外备注
    item["overseas_remark"] = response["overseasRemark"]
    # 9.期货/现货
    item["provide_type"] = "现货" if response["provideWayId"] == 2 else "期货"
    # 10.发票类型
    item["invoice_type"] = "带发票" if response["invoiceType"] == 1 else "不带发票"
    # 11.出货方式
    item["shipping_method"] = "可散出" if response["sellType"] == 0 else "整出"
    # 12.定金
    item["deposit"] = str(response["deposit"]) + "%"
    # 13.国家id
    item["country_id"] = str(response["countryId"])
    # 14.国家
    item["country"] = response["countryName"] if response["countryName"] != "国产" else "中国"
    # 15.厂号
    item["factory_no"] = str(response["factoryNo"]) if response["factoryNo"] != "正规" else ""
    # 16.品名
    item["cate_name"] = str(response["cateName"])
    # 17.肥瘦比例
    item["fat_to_thin_ratio"] = str(response["scale"])
    # 18.联系人
    item["contact_person"] = response["userName"]
    # 19.联系电话
    item["phone"] = str(response["userPhone"])
    # 20.交易员
    item["trader_name"] = str(response["trader_name"])
    # 21.交易员电话
    item["trader_phone"] = str(response["trader_phone"])
    # 22.数据类型
    item["data_type"] = "供应"
    # 23.来源
    item["data_source"] = "找牛网"
    # 24.插入时间
    item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(item)
    insert_mysql(item)


def get_list_data():
    url = "https://api.zhaoniuw.com/client/good/queryList"
    headers = {
        'Host': 'api.zhaoniuw.com',
        'Content-Length': '43',
        'Authorization': 'Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFMyNTYifQ.eyJ1c2VySWQiOiJmODMzMDU5MDIyZjM0NGVjYjgzMTIzYTIzYTQyY2JiZCIsImV4cCI6MTcyNDIyOTMwMiwibmJmIjoxNjM3ODI5MzAyfQ.aArUqF7fxD600ce5WORwExp0clXGw8h3kqEcHLCYpQs',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'content-type': 'application/json',
        'znw-from-code': '1',
        'Referer': 'https://servicewechat.com/wxeb62b9e0b2917813/38/page-frame.html',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    for page_num in range(1, 1000):
        json_data = {
            "pageNumber": page_num,
            "pageSize": 10,
            "goodType": 2
        }
        ip = random.choice(ip_list)
        res = requests.post(url=url, headers=headers, json=json_data,
                            proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()
        if res["data"]["list"]:
            for per_id in res["data"]["list"]:
                get_detail_data(per_id["id"])


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_list_data()
    cursor.close()
    conn.close()
