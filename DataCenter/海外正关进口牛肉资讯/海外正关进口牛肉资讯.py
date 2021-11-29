import datetime
import random
import threading
import time
from lxml import etree
import requests
from queue import Queue
from transform_url import transform_url
from get_proxies import get_ip_list
import pymysql
import redis

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=4)
redis_dict_key = 'ods_hyd_imported_beef_information'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key,
                       item['title'] + "-" + item["create_date"]):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key,
                     item['title'] + "-" + item["create_date"], 0)
        sql = 'insert into ods_hyd_imported_beef_information(title,create_date,content,insert_time,data_source)values (%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["title"], item["create_date"], item["content"], item["insert_time"],
            item["data_source"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_detail_data(detail_url_list, id):
    """
    抓取详情页
    :param detail_url_list:
    :param id:
    :return:
    """
    while True:
        url = detail_url_list.get()  # Queue队列的get方法用于从队列中提取元素
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36",
            'Connection': 'close'
        }
        item = dict()
        ip = random.choice(ip_list)
        res = requests.get(url=url, headers=headers, proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]})
        res.encoding = "utf-8"
        response = etree.HTML(res.text)
        try:
            # 提取标题
            item["title"] = response.xpath('.//div[@id="printableview"]/h1/text()')[0]
            # 发布时间
            item["create_date"] = response.xpath('.//div[@class="n_tit"]//span[3]/text()')[0].replace("【", "").replace(
                "发布日期：", "")
            # 提取内容
            p_list = response.xpath('.//div[@id="cntrBody"]//text()|.//div[@id="cntrBody"]//img/@src')
            content_list = []
            for i in p_list:
                if "http" in i:
                    img_url = "http://www.hyd988.com/" + i
                    new_img_url = transform_url(img_url)
                    content_list.append(new_img_url)
                else:
                    content_list.append(i)
            item["content"] = ''.join(content_list)
            # 插入时间
            item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 来源
            item["data_source"] = "海运达贸易"
            print(item)
            insert_mysql(item)
            print('-' * 100)
        except:
            pass


def get_list_data(queue):
    """
    抓取文章列表页
    :param queue:
    :return:
    """
    for page_num in range(1, 43):
        url = "http://www.hyd988.com/nrzx-{}.html".format(page_num)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36",
            "Referer": "http://www.hyd988.com/nrzx-2.html",
            'Connection': 'close'
        }
        ip = random.choice(ip_list)
        res = requests.get(url=url, headers=headers,proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).text
        response = etree.HTML(res)
        detail_url_list = response.xpath('//div[@class="text"]/h2/a/@href')
        for detail_url in detail_url_list:
            queue.put(detail_url)


if __name__ == '__main__':
    ip_list = get_ip_list()
    detail_url_queue = Queue(maxsize=10)  # 用Queue构造一个大小为1000的线程安全的先进先出队列
    # 创造四个线程
    thread = threading.Thread(target=get_list_data, args=(detail_url_queue,))  # A线程负责抓取列表url
    html_thread = []
    for i in range(3):
        thread2 = threading.Thread(target=get_detail_data, args=(detail_url_queue, i))
        html_thread.append(thread2)  # B、C、D线程抓取文章详情
    start_time = time.time()
    # 启动四个线程
    thread.start()
    for i in range(3):
        html_thread[i].start()
    # 等待所有线程结束，thread.join()函数代表子线程完成之前，其父进程一直处于阻塞状态
    thread.join()
    for i in range(3):
        html_thread[i].join()
    cursor.close()
    conn.close()
    redisDB.close()
    print("last time: {} s".format(time.time() - start_time))  # 等A、B、C、D四个线程都结束后，在主进程中计算总爬取时间。
