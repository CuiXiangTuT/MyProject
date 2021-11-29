"""
第三方：
    VReadTech
    瓦斯阅读
    清博数据
    极致了数据
    新榜数据
    微小宝
    众阅
"""
import random
import time
from datetime import datetime
import pymysql
import redis
import requests
from selenium import webdriver
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_weixin_gongzhonghao_mririrouwen'


# 获取讯代理IP
def getIp():
    xdl_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=913d4f4b67e24be0998a3eb344ff732b&orderno=YZ2021923652gUFZCj&returnType=2&count=10'
    ipListData = requests.get(url=xdl_url).json()
    ipList = []
    ipList.clear()
    # 将ip以字典的形式添加至ip池
    for everyIp in ipListData['RESULT']:
        ipList.append({
            'ip': everyIp['ip'],
            'port': everyIp['port']
        })
    return ipList


# 5.放入数据库
def insertMysql(item):
    if redisDB.hexists(redis_dict_key, str(item['title']) + '-' + str(item['publishTime'])):
        print('已存在该数据，不作处理~~~')
    else:
        redisDB.hset(redis_dict_key, str(item['title']) + '-' + str(item['publishTime']), 0)
        sql = "insert into ods_weixin_gongzhonghao(title,publishTime,isOriginalArticle,author,content,gzhSource,originalURL,insertTime) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
            item['title'], item['publishTime'], item['isOriginalArticle'], item['author'], item['content'],
            item['gzhSource'],item['originalURL'], item['insertTime']))
        conn.commit()
        print('数据正在插入，请稍后...')


# 4.生成新的url
def getImgUrl():
    Ctoken = getToken()
    url = 'http://123.57.104.184:7003/upload/picture'

    headers = {
        'Referer': 'http://123.57.104.184:7003/doc.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
        "Authorization": Ctoken
    }

    data = {
        'file': '(binary)',
        'Authorization': Ctoken,
        'app_code': '',
        'version': '',
    }
    files = {'file': ('a.jpg', open('./imgFile/a.png', 'rb'))}
    # proxyIP = random.choice(ipList)
    # newImgUrl = requests.post(url=url, headers=headers, data=data, files=files,proxies={'http': str(proxyIP['ip']) + ":" + str(proxyIP['port'])}).json()['data']['path']
    newImgUrl = requests.post(url=url, headers=headers, data=data, files=files).json()['data']['path']
    return newImgUrl


# 3.获取token
def getToken():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome = webdriver.Chrome(options=chrome_options)
    # chrome = webdriver.Chrome()
    chrome.get(
        'http://123.57.104.184:7003/doc.html#/default/[%E6%A8%A1%E5%9D%97]%E7%94%A8%E6%88%B7%E6%A8%A1%E5%9D%97/createAuthenticationTokenUsingPOST')
    chrome.maximize_window()
    time.sleep(1)
    chrome.find_element_by_xpath('//ul[@id="myTab-tabs-left"]//li[2]').click()
    time.sleep(1)
    chrome.find_element_by_xpath(
        '//textarea[contains(@class,"form-control") and contains(@class,"p-value") and contains(@class,"sbu-debug-input-true")]').clear()
    chrome.find_element_by_xpath(
        '//textarea[contains(@class,"form-control") and contains(@class,"p-value") and contains(@class,"sbu-debug-input-true")]').send_keys(
        '{"appCode": "","code": "","codeId": 0,"isNewUser": true,"loginName": "13206693334","password": "qwe123","type": 1}')
    chrome.find_element_by_xpath(
        '//input[contains(@class,"form-control") and contains(@class,"p-value") and contains(@class,"p-header") and contains(@class,"sbu-debug-input-false")]').send_keys(
        'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzIwNjY5MzMzNCIsImF1ZCI6IntcImFsbE51bVwiOjAsXCJidXlOdW1cIjowLFwiaWRlbnRpdHlUeXBlXCI6MixcImlzUmVhbFwiOnRydWUsXCJvZmZlckJvb2xlYW5cIjpmYWxzZSxcInBob25lTm9cIjpcIjEzMjA2NjkzMzM0XCIsXCJzdXBwbHlOdW1cIjowLFwic3lzdGVtTXNnQm9vbGVhblwiOnRydWUsXCJzeXN0ZW1Nc2dEYXRlU3RyXCI6XCIyMDIxLTA5LTA5XCIsXCJ1aWRcIjpcIjcyYTc2N2NhNDE1MTQyYzliMzgzYjY1ZmEzMThiYzI1XCIsXCJ1c2VySWRcIjpcIjg2OTU0NDg4NFwiLFwidXNlck5hbWVcIjpcIjcuQU5HXCJ9IiwiZXhwIjoxNjMxODQwOTAzLCJpYXQiOjE2MzEyMzYxMDN9.vd_mqjsMn4hDCZ3o9Wd-ASvE6YKaSEHBVDFlNgZYOe723JmURtclobS7OhbN-BCZKF2gfPosWbarkFJYZrJmjg')
    time.sleep(1)
    chrome.find_element_by_xpath(
        '//button[contains(@class,"btn") and contains(@class,"btn-default") and contains(@class,"btn-primary") and contains(@class,"btnRequest")]').send_keys(
        Keys.ENTER)
    time.sleep(1)
    Ctoken = chrome.find_element_by_xpath(
        '//div[contains(@class,"ace_layer") and contains(@class,"ace_text-layer")]//div[@class="ace_line_group"][5]').text
    CtokienStr = Ctoken.strip().replace(',', '')[9:].replace(" ", "").replace('\n', '').replace('\t', '')
    return CtokienStr


def getDetailData(url):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome = webdriver.Chrome(options=chrome_options)
    chrome.get(url)
    pageSource = chrome.page_source
    response = etree.HTML(pageSource)
    # 是否含有原创
    try:
        item['isOriginalArticle'] = response.xpath('.//span[@id="copyright_logo"]//text()')[0]
    except:
        item['isOriginalArticle'] = ''
    # 作者
    try:
        item['author'] = response.xpath('.//div[@class="rich_media_meta_list"]/span/text()')[0].strip()
    except:
        item['author'] = ''

    # 内容
    sectionList = response.xpath('//div[@id="js_content"]/section|//div[@id="js_content"]/p')
    cokk = {}
    for sectionIndex in range(len(sectionList)):
        sectionStr = etree.tostring(sectionList[sectionIndex]).decode("utf-8")
        try:
            if 'img' in sectionStr and 'class="mp-video-player"' not in sectionStr:
                originalImgUrl = sectionList[sectionIndex].xpath('./img/@data-src')[0]
                # img做替换
                # 把该图片保存到本地
                headers = {
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
                }
                imgContent = requests.get(url=originalImgUrl, headers=headers)
                # 写入到本地
                f = open('./imgFile/a.png', 'wb')
                f.write(imgContent.content)
                print('正在生成新的图片链接，请稍等...')
                # 开始生成新的图片url
                newImgUrl = getImgUrl()
                cokk['para' + str(sectionIndex)] = [newImgUrl]
                print('图片链接已生成...')
            else:
                cokk['para' + str(sectionIndex)] = sectionList[sectionIndex].xpath('.//text()')
        except:
            pass

    k = []
    for v in cokk.values():
        if len(v) == 0:
            v = '<br/>'
        elif len(v) > 1:
            v = ' '.join(v) + '<br/>'
        else:
            v = ''.join(v) + '<br/>'
        k.append(v)
    item['content'] = ''.join(k).replace('\n', '<br/>')
    item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if len(item) > 3:
        print(item)
        insertMysql(item)
    else:
        pass


def getListData():
    url = 'https://newrank.cn/xdnphb/detail/v1/rank/article/lists'

    headers = {
        'cookie': 'tt_token=true; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1634197575; UM_distinctid=17c7dc4157e929-0c13d9b68e40c3-6d56732a-1fa400-17c7dc4157f4e7; CNZZDATA1253878005=47512762-1634190697-https%253A%252F%252Fwww.newrank.cn%252F%7C1634190697; token=553389DE63B945278FFCA5C974E21BE2; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1634197599; tt_token=true',
        'origin': 'https://newrank.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
    }
    data = {

        'account': 'roujiaosuo',
        'nonce': '32fea9cd0',
        'xyz': 'f3b30155e1a7b6a0a5e2ab742ed30f5d',

    }
    ip = random.choice(ipList)
    jsonTotalList = requests.post(url=url, headers=headers, data=data,
                                  proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['value']['articles']

    for perJson in jsonTotalList[0]:
        # 标题
        item['title'] = perJson['title']
        # 时间
        item['publishTime'] = perJson['publicTime']
        # url
        detailURL = perJson['url']
        item['originalURL'] = detailURL
        getDetailData(detailURL)


if __name__ == '__main__':
    item = {}
    item['gzhSource'] = '每日肉闻'
    ipList = getIp()
    getListData()
