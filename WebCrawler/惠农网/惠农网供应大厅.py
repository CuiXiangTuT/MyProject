import requests
from requests import session
from lxml import etree
from selenium import webdriver

# url = 'https://www.cnhnb.com/p/niurou/'
# headers = {
# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'Accept-Encoding':'gzip, deflate, br',
# 'Accept-Language':'zh-CN,zh;q=0.9',
# 'Cache-Control':'max-age=0',
# 'Connection':'keep-alive',
# 'Cookie': 'deviceId=5481276-a4eb-4305-852d-1e23fb671; sessionId=S_0KTUSNHQC8YWGM28; Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c=1631954226,1632272070,1632274864,1632282578; hnUserTicket=8468fd4c-c852-4667-a91a-ec43809a192c; hnUserId=883248472; Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c=1632282601',
# 'Host':'www.cnhnb.com',
# 'If-None-Match':'"1f484-ROIISghOjy0EqWeIVe1hQwQwFOk"',
# 'Referer':'https://www.cnhnb.com/p/niurou/',
# 'sec-ch-ua':'"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
# 'sec-ch-ua-mobile':'?0',
# 'sec-ch-ua-platform':'"Windows"',
# 'Sec-Fetch-Dest':'document',
# 'Sec-Fetch-Mode':'navigate',
# 'Sec-Fetch-Site':'same-origin',
# 'Sec-Fetch-User':'?1',
# 'Upgrade-Insecure-Requests':'1',
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
# }
# session = session()
# response = session.get(url=url,headers=headers)
# cookies = response.cookies.get_dict()
# html = etree.HTML(response.text)
# urlList = html.xpath('//div[@class="supply-item"]/div/a/@href')
# print(cookies)

# for per_url in urlList:
#     detail_url = 'https://www.cnhnb.com'+per_url
#
#     chrome = webdriver.Chrome()
#     chrome.add_cookie()

chrome = webdriver.Chrome()
cookie_deviceId={'name':'deviceId','value':'b25c886-ff33-4ca9-9977-ee95c47be','domain': 'www.cnhnb.com','path': '/'}
cookie_Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c={'name':'Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c','value':'1632284099','domain': '.cnhnb.com','path': '/'}
cookie_Hm_lvt_9aa0ee2c8e00d046f6d1631cf46da4b6={'name':'Hm_lvt_9aa0ee2c8e00d046f6d1631cf46da4b6','value':'1631674382','domain': '.www.cnhnb.com','path': '/'}
cookie_Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c={'name':'Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c','value':'1631673979,1631674382,1632284074','domain': '.cnhnb.com','path': '/'}
cookie_Hm_lvt_hnUserId={'name':'hnUserId','value':'883248472','domain': '.cnhnb.com','path': '/'}
cookie_Hm_lvt_hnUserTicket={'name':'hnUserTicket','value':'fe26ac7d-dae9-48f2-94f0-6405fd0e8bc9','domain': '.cnhnb.com','path': '/'}
cookie_Hm_lvt_sessionId={'name':'sessionId','value':'S_0KTUZSH7A41OX59O','domain': 'www.cnhnb.com','path': '/'}

chrome.add_cookie(cookie_deviceId)
chrome.add_cookie(cookie_Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c)
chrome.add_cookie(cookie_Hm_lvt_9aa0ee2c8e00d046f6d1631cf46da4b6)
chrome.add_cookie(cookie_Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c)
chrome.add_cookie(cookie_Hm_lvt_hnUserId)
chrome.add_cookie(cookie_Hm_lvt_hnUserTicket)
chrome.add_cookie(cookie_Hm_lvt_sessionId)
chrome.get('https://www.cnhnb.com/gongying/6038342/')