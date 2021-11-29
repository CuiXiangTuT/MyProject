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
redis_dict_key = 'ods_bifu_beef_news'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key,
                       item['news_title'] + "-" + item["news_publish_time"] + "-" +
                       item["news_title_pic"]):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key,
                     item['news_title'] + "-" + item["news_publish_time"] + "-" +
                     item["news_title_pic"], 0)
        sql = 'insert into ods_bifu_beef_news(news_title,news_title_pic,news_publish_time,news_context,insert_time,data_source)values (%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["news_title"], item["news_title_pic"], item["news_publish_time"], item["news_context"],
            item["insert_time"], item["data_source"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_detail_news(news_id, item):
    """
    获取资讯详情
    :param news_id: 新闻id参数
    :return:
    """
    url = "https://www.beeftochina.com.cn/api/SystemApi/GetBtcInfoDetail"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
    }
    json_data = {"MessageID": "4e51cc53-adc3-44c3-9790-78e2fabdcac6", "MessageType": 7000000002,
                 "Data": {"NewsID": str(news_id), "UserID": "danaodaiyangyang", "RelevanceID": str(news_id)}}
    ip = random.choice(ip_list)
    res = requests.post(url=url, headers=headers, json=json_data,
                        proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["Data"]["Row"]
    item["news_context"] = res["NewsContext"].replace("【来源: BTC必孚(中国) 】", "")
    item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    item["data_source"] = "BTC"
    print(item)
    insert_mysql(item)


def get_beef_news():
    """
    获取牛肉资讯信息
    :return:
    """
    url = "https://www.beeftochina.com.cn/api/SystemApi/GetBtcInfoNewsBySection"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
    }
    for page_num in range(1, 50):
        json_data = {"MessageID": "f713532b-ed56-4972-8981-45ff7d6f845c", "MessageType": 7000000004,
                     "Data": {"PageNum": page_num, "PageSize": 10, "KeyWords": "", "NewsLanguageCode": "zh-CN",
                              "Type": "_beefnewsandevents"}}
        item = dict()
        res = requests.post(url=url, headers=headers, json=json_data).json()["Data"]["Rows"]
        for per_json in res:
            # 标题
            item["news_title"] = per_json["NewsTitle"]
            # 列表页图片
            item["news_title_pic"] = per_json["NewsTitlePic"]
            # 发布时间
            item["news_publish_time"] = per_json["NewsDateTime"]
            news_id = per_json["NewsID"]
            get_detail_news(news_id, item)


if __name__ == '__main__':
    ip_list = get_ip_list()
    get_beef_news()
