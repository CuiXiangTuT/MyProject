import requests
from lxml import etree
import pymysql
import redis

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc-ods", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=3)
redis_dict_key = 'ods_country_code'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, str(item["country_area"]) + "-" + str(item["english_name"])):
        print('已存在该数据，不作处理~~~')
    else:
        redisDB.hset(redis_dict_key, str(item["country_area"]) + "-" + str(item["english_name"]), 0)
        sql = "insert into ods_country_code(iternational_code,country_area,english_name,phone_code) values(%s,%s,%s,%s)"
        cursor.execute(sql, (item['iternational_code'], item['country_area'], item['english_name'], item['phone_code']))
        conn.commit()
        print('数据正在插入，请稍后...')


def get_country_code():
    item = dict()
    url = "https://www.chinassl.net/ssltools/country-code.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
    }

    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    response = etree.HTML(res.text)
    table_data = response.xpath("//tbody//tr")
    for table_tr in table_data:
        try:
            item["iternational_code"] = table_tr.xpath("./td[1]/text()")[0]
        except:
            item["iternational_code"] = ""
        try:
            item["country_area"] = table_tr.xpath("./td[2]/text()")[0]
        except:
            item["country_area"] = ""
        try:
            item["english_name"] = table_tr.xpath("./td[3]/text()")[0]
        except:
            item["english_name"] = ""
        try:
            item["phone_code"] = table_tr.xpath("./td[4]/text()")[0]
        except:
            item["phone_code"] = ""
        insert_mysql(item)


if __name__ == '__main__':
    get_country_code()
