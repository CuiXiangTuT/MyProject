import datetime
import re
import requests
from lxml import etree
import pymysql
import redis

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc-ods", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redis_db = redis.Redis(host='127.0.0.1', port=6379, db=3)
redis_data_dict = 'ods_china_yangyangwang'


def insert_mysql(item):
    if redis_db.hexists(redis_data_dict, item['publish_time'] + '-' + item['price'] + "-" + item["market"]):
        print('该数据已存在，不做处理...')
    else:
        redis_db.hset(redis_data_dict, item['publish_time'] + '-' + item['price'] + "-" + item["market"], 0)
        sql = 'insert into ods_china_yangyangwang(title,publish_time,product,price,market,insert_time)values (%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['title'], item['publish_time'], item['product'], item['price'], item["market"],
            item['insert_time']))
        conn.commit()
        print('该数据正在插入，请稍等...')


def get_page_list():
    """
    获取列表页链接
    :return: page_list
    """
    for i in range(1, 17):
        url = "http://www.zgyangyang.com/baojia/yangjia/list" + str(i) + ".html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
        }
        res = requests.get(url=url, headers=headers).text
        response = etree.HTML(res)
        page_list = response.xpath('//div[@class="catlist"]/ul/li//a/@href')
        return page_list


def get_detail_page(page_list):
    """
    获取详情页数据
    :param page_list:列表页
    :return:
    """
    item = dict()
    for page_url in page_list:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
        }
        res = requests.get(url=page_url, headers=headers)
        res.encoding = "utf-8"
        response = etree.HTML(res.text)
        # 标题
        item["title"] = response.xpath('//h1[@class="title"]/text()')
        # 发布时间
        publish_time = response.xpath('//div[@class="info"]//text()')[1]
        text = response.xpath('//div[@class="content"]/table/tbody/tr')[1:]
        item["publish_time"] = re.search(r"(\d{4}-\d{1,2}-\d{1,2})", publish_time).group()
        for per_data in text:
            item["product"] = per_data.xpath("./td[1]/text()")[0]
            price = ''.join(per_data.xpath("./td[2]//text()"))
            item["price"] = lambda price: re.search("\d+(\.\d+)?",price).group()
            item["market"] = per_data.xpath("./td[3]/text()")[0]
            item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # insert_mysql(item)
            print(item)

if __name__ == '__main__':
    page_list = get_page_list()
    get_detail_page(page_list)
