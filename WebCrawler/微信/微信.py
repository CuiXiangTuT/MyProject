import os
import re
import threading
import time

import emoji
import redis
from lxml import etree
import pandas as pd
import pymysql
from datetime import datetime
from queue import Queue
from threading import Thread


# 读取mysql中city的数据
def read_mysql_city():
    mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
    data_cities = pd.read_sql('select * from d_bs_city;', con=mysql_cn)
    return list(data_cities['CITY_NAME'])


def read_mysql_product1():
    mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
    data_product = pd.read_sql('select * from d_supply_product_class where pid !=0;', con=mysql_cn)
    return list(zip(data_product['class_name'], data_product['pid']))


# 读取mysql中country的数据
def read_mysql_country():
    mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
    data_cities = pd.read_sql('select * from d_country;', con=mysql_cn)
    return list(data_cities['name'])


# 读取mysql中province的数据
def read_mysql_province():
    mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
    data_cities = pd.read_sql('select * from d_bs_province;', con=mysql_cn)
    return list(data_cities['PROVINCE_NAME'])


# 读取mysql中ods_supply_product_class中的数据
def read_mysql_product():
    mysql_cn = pymysql.connect(host='10.10.107.7', user='root', password='xinqian@saibao', db='bigdata', port=3306)
    data_product = pd.read_sql('select * from d_supply_product_class where pid !=0;', con=mysql_cn)
    return list(data_product['class_name'])


def insert_mysql(item):
    if r_db.hexists(redis_data_dict,
                    str(item['company_name']) + '-' + str(item['buy_supply']) + '-' + str(item['product']) + '-' + str(
                        item['timeText'])):
        print('说明数据库中已经存在该数据，直接pass...')
        pass
    else:
        r_db.hset(redis_data_dict,
                  str(item['company_name']) + '-' + str(item['buy_supply']) + '-' + str(item['product']) + '-' + str(
                      item['timeText']), 0)
        sql = 'insert into ods_weixin_lastest(company_name,phone,weixin_user_id,location,changhao,buy_supply,timeText,product,pid,content,cur_time,original_content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['company_name'], item['phone'], item['weixin_user_id'], item['location'],
            item['changhao'], item['buy_supply'], item['timeText'],
            item['product'], item['pid'], item['content'], item['cur_time'], item['original_content']))
        db.commit()


# 定义一个方法，用来对字符串进行切分
def split_data(l, ls):
    # 定义一个空的列表用来存储下标
    s_index = []
    t_index = []
    # 遍历每一个地区
    for c in range(len(l)):
        # 获取自定义字符串中的每一个字符串
        for s in range(len(ls) - 2):
            # 判断当前文字是否能与country中的元素的单个字符相匹配
            # 可以对当前列表中的元素名的长度做条件判断
            if len(l[c]) == 2:
                if ls[s:s + 2] == l[c]:
                    # print("这是zoo_str中与hall_list里单个元素的每个字符相同的下标：", s)
                    s_index.append(s)
                    t_index.append((s, s + 2))
            elif len(l[c]) == 3:
                if ls[s:s + 3] == l[c]:
                    # print("这是zoo_str中与hall_list里单个元素的每个字符相同的下标：", s)
                    s_index.append(s)
                    t_index.append((s, s + 3))
                elif ls[s:s + 2] + '省' == l[c]:
                    s_index.append(s)
                    t_index.append((s, s + 2))
                elif ls[s:s + 2] + '市' == l[c]:
                    s_index.append(s)
                    t_index.append((s, s + 2))

    else:
        s_index.append(len(ls))

    a_l = sorted(map(sorted, t_index))
    # 用来存储地址
    v = []

    for a in a_l:
        v.append(ls[a[0]:a[1]])

    return sorted(s_index), v


# 对长字符串进行切分，并按照s_index的元素数据位置进行切分
def split_str(new_index, ls):
    # 定义一个新的空列表用来存储重新分割后的长字符串
    new_long_str = []
    if len(new_index) == 1:
        new_long_str.insert(0, ls)
    else:
        # 将long_str字符串按照s_index做字符串的切割
        for i in range(len(new_index)):
            if i + 1 < len(new_index):
                new_long_str.append(ls[new_index[i]:new_index[i + 1]])
            if i == new_index[-1]:
                new_long_str.append(ls[new_index[i]:])
        if new_index[0] != 0:
            new_long_str.insert(0, ls[:new_index[0]])
    return new_long_str


# 开始对抽离出来的数据进行解析，分解
def decompose_str(item, s):
    if '肥牛1，2，3号' in s:
        s = s.replace('肥牛1，2，3号', '肥牛一号，肥牛二号，肥牛三号')
    if '肥牛一号，二号，三号' in s:
        s = s.replace('肥牛一号，二号，三号', '肥牛一号，肥牛二号，肥牛三号')
    if '1，2，3，4号' in s:
        s = s.replace('1，2，3，4号', '一号，二号，三号')
    if 'wxid' in s:
        s = s.replace('wxid', '')
    if '4w0yk4xpi11t22' in s:
        s = s.replace('4w0yk4xpi11t22', '')
    if '里子干净' in s:
        s = s.replace('里子干净', '')
    if '无油' in s:
        s = s.replace('无油', '')
    if '三层无冰' in s:
        s = s.replace('三层无冰', '')
    if '现货万邦' in s:
        s = s.replace('现货万邦', '')
    if '一号，二号，三号肉统肥膘':
        s = s.replace('一号，二号，三号肉统肥膘', '一号肉统肥膘，二号肉统肥膘，三号肉统肥膘')

    # 电话
    pattern_p = re.compile('(?<!\d)(1\d{10})(?!\d)')
    if re.findall(pattern_p, s):
        phone = re.findall(pattern_p, s)[0]
        s = re.sub(phone, '', s)

    pattern = re.compile('(\d{1,8})')
    # 匹配到所有的厂号
    dec_data = re.findall(pattern, s)
    # 拿到厂号所在位置的下标，注意是个元组
    dec_t_data = [(i.start(), i.end()) for i in re.finditer('(\d{1,8})', s)]
    for i in range(len(dec_t_data)):
        # 厂号
        changhao_no = dec_data[i]
        # 后续数据
        if i < len(dec_t_data) - 1:
            # 后续数据的分割
            d_data = s[dec_t_data[i][1]:dec_t_data[i + 1][0]]

            if '厂' in d_data:
                d_data = d_data.replace('厂', '')
            if '：' not in d_data:
                d_data = d_data.replace('：', '，')

            de_data = d_data.strip().split('，')
            if de_data[-1] == '':
                de_data = de_data[:-1]

            for k in range(len(de_data)):

                if k != len(de_data) - 1 and de_data[k] == "":
                    while k < len(de_data) - 1:
                        de_data[k] = de_data[k + 1]
                        k = k + 1

                elif k == len(de_data) - 1 and de_data[k] == '':
                    pass
                else:
                    if '吨' in de_data[k] or '柜' in de_data[k] or '件' in de_data[k] or '新货' in de_data[k] or '联系' in \
                            de_data[k] or '单品给价就卖' in de_data[k] or '期货' in de_data[k] or '现货' == de_data[k] or '价格' in \
                            de_data[k] or '比' in de_data[k] or '出秤高' in de_data[k] or '厂' in de_data[k] or '齐全' in \
                            de_data[k] or '欢迎' in de_data[k] or 'kg' in de_data[k] or 'vl' in de_data[k] or '天' in \
                            de_data[k] or '微信同电话' in de_data[k] or '' == de_data[k] or '换群' in de_data[k] or '拆' in \
                            de_data[k] or '日期' in de_data[k] or '年' in de_data[k] or '月' in de_data[k] or '到货' in \
                            de_data[k] or '安徽' in de_data[k] or '手' == de_data[k] or '鸡' in de_data[k] or '猪' in \
                            de_data[k] or 'c' in de_data[k] or 'VL' in de_data[k] or '期货' in de_data[k] or '即到' in \
                            de_data[k] or 'v' in de_data[k] or '生' == de_data[k] or '前' == de_data[k] or '后' in de_data[
                        k] or '澳大利亚' == de_data[k] or len(de_data[k]) == 1:
                        pass
                    else:
                        item['changhao'] = changhao_no
                        item['product'] = de_data[k]
                        item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        for t in t_product:
                            if item['product'] == t[0]:
                                item['pid'] = t[1]
                                print(item)
                                insert_mysql(item)

        if i == len(dec_t_data) - 1:
            de_data = s[dec_t_data[-1][1]:]
            de_data = de_data.split('，')
            for k in range(len(de_data)):
                if k == len(de_data) - 1 and de_data[k] == '':
                    pass
                else:
                    if '吨' in de_data[k] or '柜' in de_data[k] or '件' in de_data[k] or '新货' in de_data[k] or '联系' in \
                            de_data[k] or '单品给价就卖' in de_data[k] or '期货' in de_data[k] or '现货' == de_data[k] or '价格' in \
                            de_data[k] or '比' in de_data[k] or '出秤高' in de_data[k] or '厂' in de_data[k] or '齐全' in \
                            de_data[k] or '欢迎' in de_data[k] or 'kg' in de_data[k] or 'vl' in de_data[k] or '天' in \
                            de_data[k] or '微信同电话' in de_data[k] or '' == de_data[k] or '换群' in de_data[k] or '拆' in \
                            de_data[k] or '日期' in de_data[k] or '年' in de_data[k] or '月' in de_data[k] or '到货' in \
                            de_data[k] or '安徽' in de_data[k] or '手' == de_data[k] or '鸡' in de_data[k] or '猪' in \
                            de_data[k] or 'c' in de_data[k] or 'VL' in de_data[k] or '即到' in de_data[k] or 'v' in \
                            de_data[k] or '生' == de_data[k] or '前' == de_data[k] or '后' in de_data[k] or '澳大利亚' == \
                            de_data[k] or len(de_data[k]) == 1:
                        pass
                    else:
                        item['changhao'] = changhao_no
                        item['product'] = de_data[k]
                        item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        for t in t_product:
                            if item['product'] == t[0]:
                                item['pid'] = t[1]
                                print(item)
                                insert_mysql(item)


# 对contrast_str数据进行遍历
def ergodic_data(item, contrast_str):
    if '切片机' in contrast_str:
        pass
    else:
        if '求购' in contrast_str or '采购' in contrast_str:
            item['buy_supply'] = '采购'
        if '出货' in contrast_str or '出' in contrast_str or "现货" in contrast_str:
            item['buy_supply'] = '供应'
        else:
            item['buy_supply'] = '供应'
        country_index = split_data(area_l, contrast_str)[0]
        # 获取到了每一个分割开来的数据
        new_country_str = split_str(country_index, contrast_str)
        # 获取到了已被分割的数据：形式为--->地名+产品
        # 接下来开始对new_country_str中的数据进行匹配
        t_index = split_data(area_l, contrast_str)[1]

        # for eve_data in new_country_str:
        """
            需要考虑的问题：
                1.将每个数据中的地区提取出来
                2.将产品前面（包含距离最近，即上一个）的数字作为厂号
                3.如果是单独的一个数字，则将该数字后续距离最近的一个产品作为该数字下的产品
        """
        if len(t_index) == 0:
            """
                1.如果为空，那就把当前这个列表（即列表中有数据，但是并没有地址数据通常）当做数据进行插入
            """
            s = new_country_str[0]

            item['content'] = new_country_str[0]
            item['location'] = ''
            decompose_str(item, s)



        elif len(t_index) == 1 and len(new_country_str) == 1:
            """
                2.如果只有一个地址，并且当前列表（即列表中只有一个数据，并且包含地址）长度为1
            """
            new_country_str[0] = re.sub(t_index[0], '', new_country_str[0])
            s = new_country_str[0]

            item['content'] = new_country_str[0]
            item['location'] = t_index[0]
            decompose_str(item, s)


        elif len(t_index) == 1 and len(new_country_str) != 1:
            """
                3.如果当前只有一个地址，但是列表长度不为1，那就把当前列表中的所有数据包含到当前地址里
            """
            if '国产' in new_country_str[0]:
                t_index.insert(0, '中国')
                s = ' '.join(new_country_str)

                item['location'] = t_index[0]
                item['content'] = s
                decompose_str(item, s)


            else:
                mid_data = re.sub(t_index[0], '', '，'.join(new_country_str))

                item['location'] = t_index[0]
                item['content'] = mid_data
                decompose_str(item, mid_data)


        elif len(t_index) > 1 and t_index[0] not in new_country_str[0]:
            """
                4.如果当前地址列表长度不为1，于此同时地址列表的第一个数据不在具体描述数据中（即具体描述列表里的第一个数据是其他数据（不包含地址的））
                  可以将描述数据列表中的首个数据进行提取清除，并将两个列表进行上下匹配数据，最后将提取出来的数据放置第一个数据中
            """
            if '国产' in new_country_str[0]:
                t_index.insert(0, '中国')
                zip_data = list(zip(t_index, new_country_str))
                for z in range(len(zip_data)):
                    # 拿到了后续的数据

                    des_dt = re.sub(zip_data[z][0], '', zip_data[z][1])
                    # 拿到地址
                    des_ar = zip_data[z][0]

                    item['location'] = des_ar
                    item['content'] = des_dt
                    decompose_str(item, des_dt)


            else:
                first_des = new_country_str[0]
                new_country_str.pop(0)  # 已经不存在第一个无关数据
                zip_data = list(zip(t_index, new_country_str))
                for z in range(len(zip_data)):
                    if z == 0:
                        # 拿到了后续的数据
                        des_dt = first_des + ' ' + re.sub(zip_data[z][0], '', zip_data[z][1])
                        # 拿到地址
                        des_ar = zip_data[z][0]

                        item['location'] = des_ar
                        item['content'] = des_dt
                        decompose_str(item, des_dt)

                    else:
                        # 拿到了后续的数据
                        des_dt = re.sub(zip_data[z][0], '', zip_data[z][1])
                        # 拿到地址
                        des_ar = zip_data[z][0]

                        item['location'] = des_ar
                        item['content'] = des_dt
                        decompose_str(item, des_dt)

        elif len(t_index) > 1 and t_index[0] in new_country_str[0] and len(t_index) == len(new_country_str):
            """
                5.当前地址列表长度和具体描述列表长度一致，可以直接做一一对应匹配
            """
            zip_data = list(zip(t_index, new_country_str))
            for z in range(len(zip_data)):
                # 拿到了后续的数据
                des_dt = re.sub(zip_data[z][0], '', zip_data[z][1])
                # 拿到地址
                des_ar = zip_data[z][0]

                item['location'] = des_ar
                item['content'] = des_dt
                decompose_str(item, des_dt)


def run(item, t):

    fp = open(t, 'rb')
    html = fp.read().decode('utf-8')
    selector = etree.HTML(html)
    chatitemcontent_list = selector.xpath('..//div[@class="chatItem you"]')
    for i in chatitemcontent_list:

        if i.xpath('.//div[@class="cloudContent"]/a') or i.xpath('.//div[@class="systemTip"]'):
            pass
        else:

            nickName = str(i.xpath('.//div[@class="nickName"]/text()'))
            # 匹配电话号码
            pattern = re.compile('(?<!\d)(1\d{10})(?!\d)')
            # 匹配公司或者人名
            pattern1 = re.compile('[^\u4e00-\u9fa5a-zA-Z]')

            # 电话号码
            if re.findall(pattern, nickName):
                item['phone'] = re.findall(pattern, nickName)[0]

                # 厂商联系人
                item['company_name'] = re.sub(pattern1, '', nickName).strip()

            else:
                item['phone'] = ''
                item['company_name'] = re.sub(pattern1, ' ', nickName).strip()

            # 微信号
            weixin_id = i.xpath('.//img[@class="avatar"]/@src')[0].split('/')[-1].split('.')[0]

            item['weixin_user_id'] = weixin_id

            # 匹配时间
            item['timeText'] = i.xpath('.//span[@class="timeText"]/text()')[0]

            content = i.xpath('.//pre/text()')

            if content:
                # item['original_content'] = re.sub(r':(.*?):', '', emoji.demojize(content[0])).strip()
                k = re.sub(r':(.*?):', '', emoji.demojize(content[0])).strip().split('\r\n')

                s = ''.join(k).strip()

                pattern2 = re.compile('\[(.*?)\]')
                content_list = re.sub(pattern2, '', s)
                pattern3 = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9]')
                content1 = re.sub(pattern3, ' ', content_list)
                item['original_content'] = content1
                if len(content1):
                    content2 = content1.replace('。', '').replace('，', ' ').split(' ')
                    content3 = [i for i in content2 if i != '']
                    item['content'] = '，'.join(content3)

                    contrast = item['content'].replace(' ', '')

                    # 对item['contrast']数据进行遍历
                    ergodic_data(item, contrast)
        fp.close()


if __name__ == '__main__':

    start_time = time.time()
    db = pymysql.connect(user='root', password='123456', host='127.0.0.1', database='lan', port=3306,
                         charset='utf8mb4')
    cursor = db.cursor()

    r_db = redis.Redis(host='127.0.0.1', port=6379, db=1)
    redis_data_dict = 'ods_weixin_lastest'

    queue = Queue(maxsize=1000)

    file_paths = []

    cities = read_mysql_city()
    countries = read_mysql_country()
    provinces = read_mysql_province()
    t_product = read_mysql_product1()

    products = read_mysql_product()
    additional_area = ['澳洲']

    area_l = countries + provinces + cities + additional_area



    item = {}
    file_dir = './网页格式'
    for root, dir, files in os.walk(file_dir):
        for i in files:
            t = root + '/' + i
            file_paths.append(t)

    for i in range(len(file_paths)):
        t = threading.Thread(target=run,args=(item,file_paths[i]))
        t.start()
        t.join()
    end_time = time.time()
    print('花费总时间：',end_time-start_time)

