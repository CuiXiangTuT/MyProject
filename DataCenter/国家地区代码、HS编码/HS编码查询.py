import random
from get_proxies import *
import requests
from lxml import etree
import redis
import pymysql

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc-ods", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=3)
redis_dict_key = 'ods_hs_code'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, str(item["goods_code"]) + "-" + str(item["goods_name"])):
        print('已存在该数据，不作处理~~~')
    else:
        redisDB.hset(redis_dict_key, str(item["goods_code"]) + "-" + str(item["goods_name"]), 0)
        sql = "insert into ods_hs_code(goods_code,goods_name,units,export_rebate_rate,supervision,ciq) values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (item['goods_code'], item['goods_name'],item['units'], item['export_rebate_rate'], item['supervision'], item['ciq']))
        conn.commit()
        print('数据正在插入，请稍后...')


def get_hs_code():
    """
    获取code_list列表
    :return:
    """
    for page_num in range(1, 50):
        for key_word in ["牛", "羊"]:
            url = "https://www.hsbianma.com/Search/" + str(
                page_num) + "?keywords=" + key_word + "&filterFailureCode=true"
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
            }
            ip = random.choice(ip_list)
            res = requests.get(url=url, headers=headers,proxies={"http":"http://"+ip["ip"]+":"+ip["port"]}).text
            response = etree.HTML(res)
            tr_list = response.xpath('.//tr[@class="result-grid"]')
            for tr in tr_list:
                item = dict()
                # 商品编码
                item["goods_code"] = tr.xpath('./td[1]/a/text()')[0]
                # 商品名称
                item['goods_name'] = ''.join(tr.xpath('./td[2]//text()')).strip()
                # 计量单位
                item['units'] = str(tr.xpath('./td[3]/text()')[0]).strip()
                # 出口退税率
                item['export_rebate_rate'] = str(tr.xpath('./td[4]/text()')[0]).strip()
                try:
                    # 监管条件
                    item['supervision'] = str(tr.xpath('./td[5]/text()')[0]).strip()
                except:
                    item['supervision'] = ''
                try:
                    # 检验检疫CIQ
                    item['ciq'] = str(tr.xpath('./td[6]/text()')[0]).strip()
                except:
                    item['ciq'] = ''
                print(item)
                insert_mysql(item)


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_hs_code()
