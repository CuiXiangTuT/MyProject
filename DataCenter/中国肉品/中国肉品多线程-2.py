import datetime
import random
import re
import time

import requests
from queue import Queue
from threading import Thread
from get_proxies import get_ip_list


class ChinaMeat:
    def __init__(self):
        self.list_url = "http://app.meat.hongliaowang.com/meat/query"  # 列表页的url
        self.detail_url = "http://app.meat.hongliaowang.com/meat/get"  # 详情页的url
        # 列表页的headers
        self.list_headers = {
            'channel': '',
            'os': 'ANDROID',
            'Content-Type': 'application/json; charset=UTF-8',
            'Content-Length': '96',
            'Host': 'app.meat.hongliaowang.com',
            # 'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.1',
        }
        # 详情页的headers
        self.detail_headers = {
            'authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMzUzYjA1MjA2MmMxMWVjOWI2MTAwMTYzZTM1ZmNhMyIsImlhdCI6MTYyOTk1NDY5MSwianRpIjoiIn0.Rqb9jRR-mmIiYz2WhcAnxafGVWAquWzWd8GyszmDKRE',
            'channel': '',
            'os': 'ANDROID',
            'Content-Type': 'application/json; charset=UTF-8',
            'Content-Length': '41',
            'Host': 'app.meat.hongliaowang.com',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.9.1',
        }
        # 定义一个json_data队列
        self.json_data_queue = Queue()
        # 定义一个列表页response队列
        self.json_response_queue = Queue()
        # 定义一个content队列
        self.content_queue = Queue()
        # 获取代理
        self.ip_list = get_ip_list()

    def start_url(self):
        for page_num in range(1, 3):
            json_data = {
                "category": "牛肉",
                "madein": "",
                "orderBy": "time",
                "pageIndex": page_num,
                "pageSize": 10,
                "stockAddress": ""
            }
            self.json_data_queue.put(json_data)

    def parse_url(self):
        while True:
            json_data = self.json_data_queue.get()  # 从json_data_queue中获取一个json_data
            ip = random.choice(self.ip_list)
            data_list = requests.post(url=self.list_url, headers=self.list_headers, json=json_data,
                                      proxies={"http": "http://" + ip["ip"] + ":" + ip["port"]}).json()["data"]["list"]
            for per_id in data_list:
                self.json_response_queue.put(per_id["id"])
            self.json_data_queue.task_done()  # json完成本次任务，从队列中删除

    def get_detail_data(self):
        while True:
            id_data = self.json_response_queue.get()
            json_data = {
                "id", id_data
            }
            res = requests.post(self.detail_url, headers=self.detail_headers, json=json_data).json()["data"]
            self.content_queue.put(res)

    def get_detail_json_data(self):
        while True:
            res = self.content_queue.get()
            item = dict()
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

    def run(self):
        # 开始时间
        start_time = time.time()
        thread_list = []  # 初始化一个线程列表
        json_data = Thread(target=self.start_url)  # 使用一个线程获取json_data_list
        thread_list.append(json_data)  # 添加线程到列表中
        # 提交请求，获取响应
        for i in range(10):
            t_parse = Thread(target=self.parse_url)  # 遍历一次就是用一个线程去完成请求任务
            thread_list.append(t_parse)

        # 提取数据
        for i in range(10):
            t_detail_parse = Thread(target=self.get_detail_data)  # 遍历一次就使用一个线程来完成提取数据任务
            thread_list.append(t_detail_parse)

        for i in range(10):
            detail_json_1 = Thread(target=self.get_detail_json_data)
            thread_list.append(detail_json_1)

        # 遍历线程列表
        for t in thread_list:
            t.setDaemon(True)  # 设置守护线程，确保有线程在执行，当只有守护线程时，程序运行结束
            t.start()  # 线程开始运行

        for q in [self.json_data_queue, self.json_response_queue, self.content_queue]:  # 依次遍历三个队列
            q.join()

        print("主线程运行结束")
        end_time = time.time()
        print("运行时间：", end_time - start_time)


if __name__ == '__main__':
    china_meat = ChinaMeat()
    china_meat.run()
