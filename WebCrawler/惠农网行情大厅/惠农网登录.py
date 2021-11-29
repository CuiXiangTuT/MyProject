from selenium import webdriver
from lxml import etree
from selenium.webdriver.common.keys import Keys
import time

#
# chrome = webdriver.Chrome()
# chrome.maximize_window()
# chrome.get('https://www.cnhnb.com/login/')
# chrome.find_element_by_xpath('//div[@class="tab-item"][2]').click()
# time.sleep(1)
# chrome.find_element_by_xpath('//input[@name="account2"]').send_keys('13037639858')
# time.sleep(1)
# chrome.find_element_by_xpath('//input[@name="password2"]').send_keys('13037639858cui')
# time.sleep(1)
# chrome.find_element_by_xpath('//div[@class="clause"]/i').click()
# time.sleep(2)
# chrome.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div[2]/form[2]/button').click()
# # 获取cookie
# cookies_item = chrome.get_cookies()
# cookie_str = ""
# #组装cookie字符串
# for item_cookie in cookies_item:
#     item_str = item_cookie["name"]+"="+item_cookie["value"]+"; "
#     cookie_str += item_str
# #打印出来看一下
# print(cookie_str)

page_url = 'https://www.cnhnb.com/p/niurou/'

cookie = {
    'Cookie': 'deviceId=5481276-a4eb-4305-852d-1e23fb671; sessionId=S_0KTUSNHQC8YWGM28; Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c=1631844103,1631954226,1632272070,1632274864; Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c=1632274966; hnUserTicket=7371c897-bf61-4dae-b623-c18194b95c29; hnUserId=883248472'
}
"""
Cookie: deviceId=5481276-a4eb-4305-852d-1e23fb671; sessionId=S_0KTUSNHQC8YWGM28; Hm_lvt_91cf34f62b9bedb16460ca36cf192f4c=1631844103,1631954226,1632272070,1632274864; Hm_lpvt_91cf34f62b9bedb16460ca36cf192f4c=1632274906
"""
chrome1 = webdriver.Chrome()
chrome1.add_cookie(cookie)
chrome1.get(page_url)


