from datetime import datetime
import time

import pymysql
import redis
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_jingdong_dazhuangyuan'


def insertMysql(item):
    if redisDB.hexists(redis_dict_key, item['title']):
        print('数据已存在，不做处理...')
    else:
        redisDB.hset(redis_dict_key, item['title'], 0)
        sql = 'insert into ods_jd_dazhuangyuan(title,price,insertTime) values (%s,%s,%s)'
        cursor.execute(sql, (item['title'], item['price'], item['insertTime']))
        conn.commit()


def getData():
    # 京东url
    url = 'https://www.jd.com/'
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url=url)
    driver.find_element_by_xpath('//input[@clstag="h|keycount|head|search_c"]').send_keys('大庄园')



    time.sleep(1)
    driver.find_element_by_xpath('//button[@clstag="h|keycount|head|search_a"]').click()
    time.sleep(1)
    # 滚轮滑动到最下方，获取数据
    js = "window.scrollTo(0,document.body.scrollHeight)"
    driver.execute_script(js)
    time.sleep(2)
    # 获取网页源码
    source = driver.page_source
    html = etree.HTML(source)
    li_list = html.xpath('//ul[contains(@class,"gl-warp") and contains(@class,"clearfix")]//li')
    item = {}



    for per_li in li_list:
        # 产品名
        title = per_li.xpath('.//div[contains(@class,"p-name") and contains(@class,"p-name-type-2")]//em//text()')
        item['title'] = ' '.join(title)
        # 价格
        price = per_li.xpath('.//div[@class="p-price"]/strong//i/text()')[0]
        item['price'] = price
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['source'] = '京东'
        # insertMysql(item)
        print(item)
if __name__ == '__main__':
    getData()
    cursor.close()
    conn.close()
