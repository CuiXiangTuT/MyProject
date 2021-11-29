import random
from datetime import datetime
import pymysql
import redis
from lxml import etree
import requests
from Utils.get_proxies import get_ip_list

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_weixin_gongzhonghao_niurenyide'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, str(item['title']) + '-' + str(item['publishTime'])):
        print('已存在该数据，不作处理~~~')
    else:
        redisDB.hset(redis_dict_key, str(item['title']) + '-' + str(item['publishTime']), 0)
        sql = "insert into ods_weixin_gongzhonghao(title,publishTime,isOriginalArticle,author,content,gzhSource,originalURL,insertTime) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
            item['title'], item['publishTime'], item['isOriginalArticle'], item['author'], item['content'],
            item['gzhSource'], item['originalURL'], item['insertTime']))
        conn.commit()
        print('数据正在插入，请稍后...')


def get_detail_data(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
    }
    res_text = requests.get(url=url, headers=headers).text
    response = etree.HTML(res_text)
    # 是否含有原创
    try:
        item['isOriginalArticle'] = response.xpath('.//span[@id="copyright_logo"]//text()')[0]
    except:
        item['isOriginalArticle'] = ''
    # 作者
    try:
        item['author'] = response.xpath(
            './/span[contains(@class,"rich_media_meta") and contains(@class,"rich_media_meta_text")]/text()')[0].strip()
    except:
        item['author'] = ''
    # 内容
    sectionList = response.xpath('//div[@id="js_content"]//text()|//div[@id="js_content"]//img/@data-src')

    content_list = []

    for i in sectionList:
        if 'http' in i:
            img_url = '<img src="' + i + '">'
            content_list.append(img_url)
        elif i.strip():
            content_list.append(i)
        else:
            pass
    content = '<br/>'.join(content_list)
    item['content'] = content
    item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_mysql(item)
    print(item)

def get_list_data():
    """
    获取列表页
    :return: 列表页的每一条新闻的url
    """
    url = 'https://newrank.cn/xdnphb/detail/v1/rank/article/lists'

    headers = {
        'cookie': 'tt_token=true; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1634197575; UM_distinctid=17c7dc4157e929-0c13d9b68e40c3-6d56732a-1fa400-17c7dc4157f4e7; CNZZDATA1253878005=47512762-1634190697-https%253A%252F%252Fwww.newrank.cn%252F%7C1634190697; token=553389DE63B945278FFCA5C974E21BE2; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1634197599; tt_token=true',
        'origin': 'https://newrank.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
    }
    data = {
        'account': 'beefman888',
        'nonce': 'd5ef41c3a',
        'xyz': '94f6f24cdef56ae10229c3e877e9de92',
    }
    ip = random.choice(ip_list)
    json_total_list = requests.post(url=url, headers=headers, data=data,
                                    proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['value'][
        'articles']

    for perJson in json_total_list[0]:
        # 标题
        item['title'] = perJson['title']
        # 时间
        item['publishTime'] = perJson['publicTime']
        # url
        detail_url = perJson['url']
        item['originalURL'] = detail_url
        get_detail_data(detail_url)


if __name__ == '__main__':
    ip_list = get_ip_list()
    item = dict()
    item['gzhSource'] = '牛人一得'
    dir_path = 'niurenyide'
    get_list_data()
