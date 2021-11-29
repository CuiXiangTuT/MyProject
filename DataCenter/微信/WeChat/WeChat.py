import datetime
import pymysql
import redis
from lxml import etree
import re
from get_factory import get_factory_data

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=4)
redis_dict_key = 'ods_temp_wechat'


def insert_mysql(item):
    if redisDB.hexists(item["create_date"] + "-" + item["content"], redis_dict_key):
        print("数据已入库，不作处理...")
    else:
        redisDB.hset(redis_dict_key, item["create_date"] + "-" + item["content"], 0)
        sql = 'insert into ods_temp_wechat(wechat_user_id,company,phone,create_date,content,insert_time) values (%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
        item["wechat_user_id"], item["company"], item["phone"], item["create_date"], item["content"],
        item["insert_time"]))
        print("数据正在插入，请稍后...")
        conn.commit()
    pass


def get_html_data():
    """
    读取HTML中的内容，获取信息
    :return:
    """
    item = dict()
    fp = open('../WeChatFile/Test1125.html', 'rb')
    html = fp.read().decode('utf-8')
    selector = etree.HTML(html)
    chat_item_content_list = selector.xpath('..//div[@class="chatItem you"]')
    for chat_item_content in chat_item_content_list:
        if chat_item_content.xpath('.//div[@class="cloudContent"]/a') or chat_item_content.xpath(
                './/div[@class="systemTip"]'):
            pass
        else:
            nickName = str(chat_item_content.xpath('.//div[@class="nickName"]/text()'))
            # 匹配电话号码
            pattern = re.compile('(?<!\d)(1\d{10})(?!\d)')
            # 匹配公司或者人名
            pattern1 = re.compile('[^\u4e00-\u9fa5a-zA-Z]')

            # 电话号码
            if re.findall(pattern, nickName):
                item['phone'] = re.findall(pattern, nickName)[0]

                # 厂商联系人
                item['company'] = re.sub(pattern1, '', nickName).strip()

            else:
                item['phone'] = ''
                item['company'] = re.sub(pattern1, ' ', nickName).strip()

            # 微信号
            weixin_id = chat_item_content.xpath('.//img[@class="avatar"]/@src')[0].split('/')[-1].split('.')[0]

            item['wechat_user_id'] = weixin_id

            # 匹配时间
            item['create_date'] = chat_item_content.xpath('.//span[@class="timeText"]/text()')[0]

            content_list = chat_item_content.xpath('.//pre/text()')
            content_str = ''.join(content_list)
            if '\r\n' in content_str:
                new_content_list = content_str.split('\r\n')
            else:
                new_content_list = content_list
            for content in new_content_list:
                if content != '':
                    if '、' in content.strip():
                        temp_list = content.strip().split('、')
                        for temp_data in temp_list:
                            if temp_data!='':
                                item["content"] = temp_data.strip()
                                item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                print(item)
                                insert_mysql(item)
                    elif '，' in content.strip():
                        temp_list = content.strip().split('，')
                        for temp_data in temp_list:
                            if temp_data != '':
                                item["content"] = temp_data.strip()
                                item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                print(item)
                                insert_mysql(item)
                    else:
                        item["content"] = content.strip()
                        item["insert_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(item)
                        insert_mysql(item)
            print("-" * 50)


if __name__ == '__main__':
    # 工厂的厂号列表
    factory_list = get_factory_data()
    get_html_data()
    cursor.close()
    conn.close()
