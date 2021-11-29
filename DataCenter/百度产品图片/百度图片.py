import json
import random
import time
import datetime
import redis
import pandas as pd
import pymysql
from get_proxies import *

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc-ods", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=3)
redis_dict_key = 'ods_category_img'


def get_category_list():
    """
    获取品类表
    :return: 品类列表
    """
    mysql_cn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc-ods",
                               port=3306)
    product_list = pd.read_sql('select * from dwd_comm_sku_info;', con=mysql_cn)
    return product_list["spu_name"].values


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, str(item["spu_name"])):
        print('已存在该数据，不作处理~~~')
    else:
        redisDB.hset(redis_dict_key, str(item["spu_name"]), 0)
        sql = "insert into ods_category_img(spu_name,img_name) values(%s,%s)"
        cursor.execute(sql, (item['spu_name'], item['img_name']))
        conn.commit()
        print('数据正在插入，请稍后...')


def get_img_url(spu_name_list):
    if len(spu_name_list):
        item = dict()
        for word in list(set(spu_name_list)):
            url = 'https://image.baidu.com/search/acjson'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
            }

            params = {
                'tn': 'resultjson_com',
                'logid': '11395199217591961811',
                'ipn': 'rj',
                'ct': '201326592',
                'is': '',
                'fp': 'result',
                'fr': '',
                'word': word,
                'queryWord': word,
                'cl': '2',
                'lm': '-1',
                'ie': 'utf-8',
                'oe': 'utf-8',
                'adpicid': '',
                'st': '-1',
                'z': '',
                'ic': '',
                'hd': '',
                'latest': '',
                'copyright': '',
                's': '',
                'se': '',
                'tab': '',
                'width': '',
                'height': '',
                'face': '0',
                'istype': '2',
                'qc': '',
                'nc': '1',
                'expermode': '',
                'nojc': '',
                'isAsync': '',
                'pn': '30',
                'rn': '30',
                'gsm': '1e',
                '1636533242297': '',
            }
            # ip = random.choice(ip_list)

            time.sleep(1)
            try:
                # response = requests.get(url=url, headers=headers, params=params,
                #                         proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()
                response = requests.get(url=url, headers=headers, params=params).json()
                res = json.dumps(response).replace('\\', '\\\\')
                response = json.loads(res)
                for json_data in response["data"][5:6]:
                    img_url = json_data["thumbURL"]
                    item["spu_name"] = word
                    img_name = str(int(time.time())) + ".jpg"
                    img_io = requests.get(url=img_url, headers=headers)
                    f = open('ImgFile/' + img_name, 'wb')
                    f.write(img_io.content)
                    item["img_name"] = img_name
                    insert_mysql(item)
                    print(item)
            except:
                l.append(word)


if __name__ == '__main__':
    # ip_list = get_ip_list()
    l = []
    spu_name_list = get_category_list()
    get_img_url(spu_name_list)
    print('-' * 50)
    print('数据：', l)
