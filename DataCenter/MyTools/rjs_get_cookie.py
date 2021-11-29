import json
import time

from selenium import webdriver


def get_phone():
    """
    识别电话号码
    :param url: 详情页url
    :return: 电话号码
    """
    url = "http://www.roujiaosuo.com/member/login.php"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome = webdriver.Chrome(options=chrome_options)
    # chrome = webdriver.Chrome()
    chrome.maximize_window()
    chrome.get(url=url)
    time.sleep(2)
    chrome.find_element_by_xpath('.//input[@class="reg-tel-text"]').send_keys("13037639858")
    time.sleep(1)
    chrome.find_element_by_xpath('.//input[@class="reg-powd"]').send_keys("13037639858cui")
    time.sleep(1)
    chrome.find_element_by_xpath('.//button[@type="submit"]').click()
    time.sleep(2)

    cookies = chrome.get_cookies()
    with open("cookies.json", "w") as fp:
        json.dump(cookies, fp)
    print(cookies)


if __name__ == '__main__':
    get_phone()
