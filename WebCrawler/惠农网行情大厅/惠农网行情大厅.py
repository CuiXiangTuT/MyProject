import random
import re
import time
from datetime import datetime
import pymysql
import redis
import requests
from lxml import etree
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from lxml import etree



# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_hnw_hangqingdating'

#  获取ip
def getIpList():
    ipList = []
    ipUrl = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=913d4f4b67e24be0998a3eb344ff732b&orderno=YZ2021923652gUFZCj&returnType=2&count=10'
    ipResponse = requests.get(url=ipUrl).json()["RESULT"]
    for everyIp in ipResponse:
        ipList.append({
            'ip': everyIp['ip'],
            'port': everyIp['port']
        })
    return ipList



def insertMysql(item):
    if redisDB.hexists(redis_dict_key,
                       str(item['Ctime']) + '-' + str(item['Cplace']) + '-' + str(item['price']) + '-' + str(
                           item['minSevenPrice'])):
        print('数据已存在，不做处理~~~')
    else:
        print('正在入库...')
        redisDB.hset(redis_dict_key,
                     str(item['Ctime']) + '-' + str(item['Cplace']) + '-' + str(item['price']) + '-' + str(
                         item['minSevenPrice']), 0)
        sql = "insert into ods_hnw_hangqingdating(Ctime,product,Cplace,price,dayPrice,compareBefore,maxSevenPrice,minSevenPrice,avgSevenPrice,insertTime) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
            item['Ctime'], item['product'], item['Cplace'], item['price'], item['dayPrice'], item['compareBefore'],
            item['maxSevenPrice'], item['minSevenPrice'], item['avgSevenPrice'], item['insertTime']))
        conn.commit()


def perPageData(html):
    response = etree.HTML(html)
    pattern = re.compile('：(.*)')
    # 当期均价
    dayPrice = response.xpath('//div[@class="trending-data"][1]/text()')[0].strip()
    item['dayPrice'] = re.findall(pattern, dayPrice)[0]
    # 相对比前日
    compareBefore = response.xpath('//div[@class="trending-data"][2]/text()')[0].strip()
    item['compareBefore'] = re.findall(pattern, compareBefore)[0]
    # 近7日最高价
    maxSevenPrice = response.xpath('//div[@class="trending-data"][3]/text()')[0].strip()
    item['maxSevenPrice'] = re.findall(pattern, maxSevenPrice)[0]
    # 近七日最低价
    minSevenPrice = response.xpath('//div[@class="trending-data"][4]/text()')[0].strip()
    item['minSevenPrice'] = re.findall(pattern, minSevenPrice)[0]
    # 近七日均价
    avgSevenPrice = response.xpath('//div[@class="trending-data"][5]/text()')[0].strip()
    item['avgSevenPrice'] = re.findall(pattern, avgSevenPrice)[0]
    # 插入时间
    item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insertMysql(item)


def getPageData(html):
    response = etree.HTML(html)
    spanList = response.xpath('//li[@class="market-list-item"]')

    for everySpan in spanList:
        # 时间
        item['Ctime'] = everySpan.xpath('.//span[@class="time"]/text()')[0]
        # 产品、品种
        item['product'] = everySpan.xpath('.//span[@class="product"]/text()')[0]
        # 所在产地
        item['Cplace'] = everySpan.xpath('.//span[@class="place"]/text()')[0]
        # 价格
        item['price'] = everySpan.xpath('.//span[@class="price"]/text()')[0]
        # url
        partUrl = everySpan.xpath('.//a/@href')[0]
        url = 'https://www.cnhnb.com' + partUrl
        chrome = webdriver.Chrome()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        ip = random.choice(ipList)
        chrome_options.add_argument(('--proxy-server=' + 'http://' + ip['ip'] + ':' + ip['port']))
        chrome.get(url)
        time.sleep(1)
        responseHtml = chrome.page_source
        perPageData(responseHtml)


def getList():
    wordList = ['niu', 'yang']
    pageCount = [69, 44]
    zipList = list(zip(wordList, pageCount))

    for everyZip in zipList:
        for pageNum in range(1, everyZip[1]):
            url = 'https://www.cnhnb.com/hangqing/cdlist-2001184-0-0-0-0-{}/'.format(pageNum)
            chrome = webdriver.Chrome()
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            ip  = random.choice(ipList)
            chrome_options.add_argument(('--proxy-server=' + 'http://'+ip['ip']+':'+ip['port']))
            chrome.get(url)
            time.sleep(2)
            responseHtml = chrome.page_source

            getPageData(responseHtml)



if __name__ == '__main__':
    ipList = getIpList()
    item = {}
    getList()
    cursor.close()
    conn.close()
