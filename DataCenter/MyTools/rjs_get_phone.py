import time
import uuid
from PIL import Image
from selenium import webdriver
import pytesseract



def get_phone(url):
    """
    识别电话号码
    :param url: 详情页url
    :return: 电话号码
    """
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome = webdriver.Chrome(options=chrome_options)
    # chrome = webdriver.Chrome()
    chrome.maximize_window()
    chrome.get(url=url)
    chrome.find_element_by_xpath('.//div[@id="destoon_member"]//span[2]/a').click()
    time.sleep(2)
    chrome.find_element_by_xpath('.//input[@class="reg-tel-text"]').send_keys("13037639858")
    time.sleep(1)
    chrome.find_element_by_xpath('.//input[@class="reg-powd"]').send_keys("13037639858cui")
    time.sleep(1)
    chrome.find_element_by_xpath('.//button[@type="submit"]').click()
    time.sleep(2)

    img_name = str(uuid.uuid4())
    # 全截屏进行截图保存
    chrome.save_screenshot('..\\ImgFile\\' + img_name + '.png')
    time.sleep(2)
    # 找到img标签所在的位置
    imgPhone = chrome.find_element_by_xpath('//img[@align="absmddle"]')
    left = imgPhone.location['x']  # 区块截图左上角在网页中的x坐标
    top = imgPhone.location['y']  # 区块截图左上角在网页中的y坐标
    right = left + imgPhone.size['width']  # 区块截图右下角在网页中的x坐标
    bottom = top + imgPhone.size['height']  # 区块截图右下角在网页中的y坐标
    phone = Image.open('..\\ImgFile\\' + img_name + '.png')
    # 进行区域性截图保存，名字仍为原先的，以覆盖
    phone = phone.crop((left, top, right, bottom))
    phone.save('..\\ImgFile\\' + img_name + '.png')
    chrome.quit()

    # 进行识别
    phone = pytesseract.image_to_string(Image.open('..\\ImgFile\\' + img_name + '.png'), lang='eng',
                                       config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')[:11].strip()
    return phone


if __name__ == '__main__':
    phone = get_phone('http://www.roujiaosuo.com/sell/show/799439/')
    print(phone)