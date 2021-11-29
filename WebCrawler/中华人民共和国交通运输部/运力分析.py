import random
from datetime import datetime
import pymysql
import redis
import requests
from lxml import etree
from io import BytesIO
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import Image

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()

# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_cnjtysb_yunlifenxi'


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


# 5.放入数据库
def insertMysql(item):
    if redisDB.hexists(redis_dict_key, str(item['title']) + '-' + str(item['publishTime'])):
        print('已存在该数据，不作处理~~~')
    else:
        redisDB.hset(redis_dict_key,
                     str(item['title']) + '-' + str(item['publishTime']), 0)
        sql = "insert into ods_cnjtysb_yunlifenxi(title,publishTime,html,formatData,insertTime)values (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (item['title'], item['publishTime'], item['html'],item['formatData'],item['insertTime']))
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
    files = {'file': ('yunlifenxi.jpg', open('./imgFile/yunlifenxi.png', 'rb'))}
    # proxyIP = random.choice(ipList)
    # newImgUrl = requests.post(url=url, headers=headers, data=data, files=files,proxies={'http': str(proxyIP['ip']) + ":" + str(proxyIP['port'])}).json()['data']['path']
    newImgUrl = requests.post(url=url, headers=headers, data=data, files=files).json()['data']['path']
    return newImgUrl


# 3.获取token
def getToken():
    chrome_options = Options()
    # ip = random.choice(ipList)
    # proxy_ip = str(ip['ip'])+":"+str(ip['port'])
    # chrome_options.add_argument(f"--proxy-server={proxy_ip}")
    chrome_options.add_argument('--headless')
    chrome = webdriver.Chrome(options=chrome_options)
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


# 4.获取详情页数据
def getDetailData(Chtml, Curls):
    response = etree.HTML(Chtml)
    # 标题
    item['title'] = response.xpath('//title[1]/text()')[0]
    # 定义一个空字典：contentDict = {}
    contentDict = {}
    if response.xpath('.//div[@id="content_main"]//p'):
        part_url = Curls.replace(Curls.split('/')[-1], '')[:-1]
        # 获取文章内容
        pList = response.xpath('.//div[@id="content_main"]//p')
        for perPIndex in range(len(pList)):
            partStr = etree.tostring(pList[perPIndex]).decode("utf-8")
            if 'img' in partStr:
                # 获取图片链接
                originalImgUrl_0 = pList[perPIndex].xpath('.//img/@src')[0]
                originalImgUrl = part_url + originalImgUrl_0[1:]
                # 把该图片保存到本地
                imgContent = requests.get(url=originalImgUrl)
                try:
                    # 写入到本地
                    image = Image.open(BytesIO(imgContent.content))
                    image.save('./imgFile/yunlifenxi.png')
                    print('正在生成新的图片url...请稍等')
                    # 开始生成新的图片url
                    newImgUrl = getImgUrl()
                    contentDict['p_' + str(perPIndex)] = newImgUrl
                    Chtml = Chtml.replace(originalImgUrl_0, newImgUrl)
                    print('图片链接已生成...')
                except:
                    pass
            else:
                # 直接取内容
                content = ''.join(pList[perPIndex].xpath('.//text()'))
                contentDict['p_' + str(perPIndex)] = content
        item['html'] = Chtml
        item['formatData'] = str(contentDict)
        # 插入时间
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insertMysql(item)
        print("格式化数据显示：",item['formatData'])

    elif response.xpath('.//div[@id="Zoom"]//p'):
        part_url = Curls.replace(Curls.split('/')[-1], '')[:-1]
        # 获取文章内容
        pList = response.xpath('.//div[@id="Zoom"]//p')
        for perPIndex in range(len(pList)):
            partStr = etree.tostring(pList[perPIndex]).decode("utf-8")
            if 'img' in partStr:
                # 获取图片链接
                originalImgUrl_0 = pList[perPIndex].xpath('.//img/@src')[0]
                originalImgUrl = part_url + originalImgUrl_0[1:]
                # 把该图片保存到本地
                imgContent = requests.get(url=originalImgUrl)
                # 写入到本地
                image = Image.open(BytesIO(imgContent.content))
                image.save('./imgFile/yunlifenxi.png')
                print('正在生成新的图片url...请稍等')
                # 开始生成新的图片url
                newImgUrl = getImgUrl()
                contentDict['p_' + str(perPIndex)] = newImgUrl
                Chtml = Chtml.replace(originalImgUrl_0, newImgUrl)
                print('图片链接已生成...')
            else:
                # 直接取内容
                content = ''.join(pList[perPIndex].xpath('.//text()'))
                contentDict['p_' + str(perPIndex)] = content

        item['html'] = Chtml
        item['formatData'] = str(contentDict)
        # 插入时间
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insertMysql(item)
        print("格式化数据显示：",item['formatData'])
    elif response.xpath('.//div[@id="Zoom"]//div'):
        content = ''.join(response.xpath('.//div[@id="Zoom"]//div//text()'))
        item['html'] = Chtml
        item['formatData'] = str(content)
        # 插入时间
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insertMysql(item)
    else:
        pass


# 3.获取列表页url
def getUrlList(html):
    response = etree.HTML(html)
    # 获取列表页的url
    url_list = response.xpath(
        '//div[@class="row"]/div//div[contains(@class,"list-group") and contains(@class,"tab-content")]//div[@role="tabpanel"]//a/@href')
    # 获取时间
    timeList = response.xpath('//span[@class="badge"]/text()')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
    }
    for per_url in range(len(url_list)):
        if 'jiaotongyaowen' in url_list[per_url]:
            url = 'https://www.mot.gov.cn'+ url_list[per_url][5:]
            item['publishTime'] = timeList[per_url]
            response = requests.get(url=url, headers=headers).text
            getDetailData(response, url)
        elif url_list[per_url][0]=='.' and url_list[per_url][1]=='/':
            url = 'https://www.mot.gov.cn/fenxigongbao/yunlifenxi' + url_list[per_url][1:]
            item['publishTime'] = timeList[per_url]
            response = requests.get(url=url, headers=headers).text
            getDetailData(response, url)
        else:
            url = url_list[per_url]
            item['publishTime'] = timeList[per_url]
            response = requests.get(url=url, headers=headers).text
            getDetailData(response, url)


# 2.获取列表页信息
def getListHtml():
    for pageNum in range(0, 2):
        if pageNum == 0:
            url = 'https://www.mot.gov.cn/fenxigongbao/yunlifenxi/index.html'
        else:
            url = 'https://www.mot.gov.cn/fenxigongbao/yunlifenxi/index_{}.html'.format(pageNum)
        headers = {
            'Referer': 'https://www.mot.gov.cn/fenxigongbao/yunlifenxi/index.html',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
        }

        response = requests.get(url=url, headers=headers).text
        getUrlList(response)


if __name__ == '__main__':
    item = {}
    # ipList = getIpList()
    getListHtml()
