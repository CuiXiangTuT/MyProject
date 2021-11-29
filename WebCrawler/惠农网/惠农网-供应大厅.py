from selenium import webdriver
import time
from lxml import etree
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


# 3.获取详情页面上的数据
def getDetailData(url):
    chrome = webdriver.Chrome()
    chrome.maximize_window()

    chrome.get(url)
    html = chrome.page_source
    response = etree.HTML(html)
    # 标题
    item['title'] = response.xpath('//div[@class="supply-price-show"]/div/text()')[0]
    # 更新时间
    item['updateTime'] = response.xpath('//div[contains(@class,"flex-s") and contains(@class,"t-text")]//div[2]/text()')[0][5:].replace('年','-').replace('月','-').replace('日','')
    # 价格
    item['price'] = response.xpath('//div[@class="active-p"]/text()')[0]
    # 起批量
    item['startingBatch'] = response.xpath('//div[@class="line-val"][1]/text()')[0]
    # 发货地址
    item['address'] = response.xpath('//div[@class="line-val"][2]/text()')[0].strip()
    chrome.find_element_by_xpath('//i[contains(@class,"iconfont") and contains(@class,"icon-dadianhua")]').click()
    # ActionChains(chrome).move_to_element(phone).perform()
    time.sleep(1)
    print(item)


# 2.获取页面上的url列表
def getDivList():
    chrome = webdriver.Chrome()
    chrome.maximize_window()
    for pageNum in range(50):
        chrome.get('https://www.cnhnb.com/p/niurou-0-0-0-0-{}/'.format(pageNum))
        html = chrome.page_source
        time.sleep(1)
        response = etree.HTML(html)
        divUrlList = response.xpath('//div[@class="supply-item"]/div/a/@href')
        for everyDivUrl in divUrlList:
            url = 'https://www.cnhnb.com'+everyDivUrl
            getDetailData(url)
            break
        break

# 1.获取登录之后的cookie以供后续使用
def getCookie():
    chrome = webdriver.Chrome()
    chrome.get('https://www.cnhnb.com/')
    # 最大化窗口
    chrome.maximize_window()
    time.sleep(1)
    # 查找到登陆键进行登录
    chrome.find_element_by_xpath('//div[@class="l-l"]').click()
    time.sleep(2)

    # 等待响应完成
    chrome.switch_to.frame('eye-iframe-sso-login')

    # 找到密码登录
    btn_water = chrome.find_element(By.XPATH('//*[@id="__layout"]/div/div/div/div[1]/div[1]/div[3]'))
    # 找到按钮后单击
    chrome.switch_to.frame(btn_water)
    time.sleep(2)

    # 输入账号
    # chrome.find_element_by_xpath('//input[@name="account2"]').send_keys('13037639858')
    # # 输入密码
    # chrome.find_element_by_xpath('//input[@name="password2"]').send_keys('13037639858cui')
    # # 点击同意隐私政策
    # chrome.find_element_by_xpath('//*[@id="__layout"]/div/div/div/div[1]/div[2]/div[2]/i').send_keys(Keys.ENTER)
    # time.sleep(1)
    # chrome.find_element_by_xpath('//button[@class="login-submit"]').send_keys(Keys.ENTER)



if __name__ == '__main__':
    item = {}
    getCookie()