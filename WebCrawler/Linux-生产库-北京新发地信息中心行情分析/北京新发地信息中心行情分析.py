import html
import random
from datetime import datetime
import pymysql
import redis
from lxml import etree
from io import BytesIO
from PIL import Image
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import requests

# 链接MySQL数据库
conn = pymysql.Connect(host='47.93.103.162', user='glny', password='glnybigdata2021', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_linux_xfd_hangqingfenxi'


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
        redisDB.hset(redis_dict_key, str(item['title']) + '-' + str(item['publishTime']), 0)
        sql = "insert into ods_xfd_hangqingfenxi(title,contentHtml,contentFormat,rightAuthor,leftAuthor,publishTime,insertTime) values(%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
        item['title'], item['contentHtml'], item['contentFormat'], item['rightAuthor'], item['leftAuthor'],
        item['publishTime'], item['insertTime']))
        conn.commit()
        print('数据正在插入，请稍后...')


# 4.生成新的url
def getImgUrl():
    Ctoken = getToken()
    time.sleep(2)
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


#  2.处理详情页url内容
def getDetailPage(Chtml):
    item = {}
    # html是原文章内容的页面代码
    response = etree.HTML(Chtml)
    # 获取文章标题
    item['title'] = response.xpath('//span[@class="right"]/text()')[0]
    # 获取文章内容
    divList = response.xpath('//div[@class="col-md-11"][3]/div[@class="conter_con"]//p')
    # 定义一个空字典：contentDict = {}
    contentDict = {}
    for perDivIndex in range(len(divList)):
        partStr = etree.tostring(divList[perDivIndex]).decode("utf-8")
        # print(partStr)
        # 获取段落内容，做分类处理
        if "text-indent:37px" in partStr:
            contentDict['paragraph' + str(perDivIndex)] = ''.join(divList[perDivIndex].xpath('.//span/text()'))
        elif 'text-indent: 0em' in partStr and 'img' in partStr:
            # print(partStr)
            # 原先图片链接
            originalImgUrl = divList[perDivIndex].xpath('.//img/@src')[0]
            # 把该图片保存到本地
            imgContent = requests.get(url=originalImgUrl)
            # 写入到本地
            image = Image.open(BytesIO(imgContent.content))
            image.save('./imgFile/a.png')
            # 开始生成新的图片url
            newImgUrl = getImgUrl()
            time.sleep(2)
            contentDict['paragraph' + str(perDivIndex)] = newImgUrl
            Chtml = Chtml.replace(originalImgUrl, newImgUrl)
        elif 'style="text-indent: 2em;"' in partStr:
            contentDict['paragraph' + str(perDivIndex)] = ''.join(divList[perDivIndex].xpath('.//span/text()')[0])
        else:
            contentDict['paragraph' + str(perDivIndex)] = ''


    res = etree.HTML(Chtml)
    k = res.xpath('.//div[@class="outer"]')[0]
    c = etree.tostring(k, encoding='utf-8').decode('utf-8').replace("""
                    <div class="col-md-11">&#13;
                        <a href="javascript:;" onclick="javascript:history.back(-1);">&#13;
                            <span class="navback"> &lt; 返回上一页</span>&#13;
                        </a>&#13;
                    </div>&#13;
""",'')




    # 替换之后的页面
    item['contentHtml'] = c
    # 数据格式化
    item['contentFormat'] = str(contentDict)
    try:
        # 作者（右下角）
        item['rightAuthor'] = response.xpath('.//p[@style="text-align: right;"]/text()')[0]
    except:
        item['rightAuthor'] = ''
    try:
        # 作者（左下角）
        item['leftAuthor'] = response.xpath('.//div[@class="ssss"]//div[1]/span/text()')[0]
    except:
        item['leftAuthor'] = ''
    try:
        # 发表时间
        item['publishTime'] = response.xpath('//*[@id="bbs"]/div/div/div/div[4]/div[2]/div[2]/span/text()')[0]
    except:
        item['publishTime'] = ''
    # 插入时间
    item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(item)
    insertMysql(item)


#  1.获取文章的列表url
def getUrlList():
    for pageNum in range(1, 3):
        url = 'http://www.xinfadi.com.cn/informationCenter.html?current={}'.format(pageNum)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36'
        }
        # proxyIP = random.choice(ipList)
        # response = requests.get(url=url, headers=headers,
                                # proxies={'http': str(proxyIP['ip']) + ":" + str(proxyIP['port'])}).text
        response = requests.get(url=url,headers=headers).text
        xpathResponse = etree.HTML(response)
        urlList = xpathResponse.xpath('//ul[contains(@class,"list_con") and contains(@class,"fl")]//a/@href')
        for everyUrl in urlList:
            detailUrl = 'http://www.xinfadi.com.cn' + everyUrl
            # proxyIP = random.choice(ipList)
            # detailResponse = requests.get(url=detailUrl, headers=headers,
                                          # proxies={'http': str(proxyIP['ip']) + ":" + str(proxyIP['port'])}).text
            detailResponse = requests.get(url=detailUrl,headers=headers).text
            getDetailPage(detailResponse)


if __name__ == '__main__':
    # ipList = getIpList()
    getUrlList()