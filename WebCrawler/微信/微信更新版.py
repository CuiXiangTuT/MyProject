import os
import re
import emoji
import redis
from lxml import etree
import pandas as pd
import pymysql
from datetime import datetime
from queue import Queue
from threading import Thread
import copy


# 读取mysql中city的数据
def read_mysql_city():
    mysql_cn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='lan', port=3306)
    data_cities = pd.read_sql('select * from std_cities;', con=mysql_cn)
    return list(data_cities['city'])


# 读取mysql中country的数据
def read_mysql_country():
    mysql_cn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='lan', port=3306)
    data_cities = pd.read_sql('select * from std_countries;', con=mysql_cn)
    return list(data_cities['country'])


# 读取mysql中province的数据
def read_mysql_province():
    mysql_cn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='lan', port=3306)
    data_cities = pd.read_sql('select * from std_provinces;', con=mysql_cn)
    return list(data_cities['province'])


# 读取mysql中ods_supply_product_class中的数据
def read_mysql_product():
    mysql_cn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='lan', port=3306)
    data_product = pd.read_sql('select * from goods;', con=mysql_cn)
    return list(data_product['goodsName'])


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
        sql = 'insert into ods_weixin_update(company_name,phone,weixin_user_id,location,changhao,buy_supply,timeText,product,content,cur_time,original_content) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['company_name'], item['phone'], item['weixin_user_id'], item['location'],
            item['changhao'], item['buy_supply'], item['timeText'],
            item['product'], item['content'], item['cur_time'], item['original_content']))
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
        new_long_str.clear()
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
def decompose_str(item, content):
    # 第一步：对content中的脏数据，例如x月x号进行去除
    pattern_date = re.compile(
        '(\d){1,2}月(\d){1,2}号|(\d){1,2}月|(\d){1,4}柜|(\d){1,4}吨|(\d){1,5}件|(\d){1,5}比例|(\d){1,3}号|(\d){1,5}公斤|(\d){1,5}条|(\d){1,5}切|(\d){1,3}vl|(\d){1,3}VL|(\d){1,4}V|(\d){1,3}D|(\d){1,3}CL|wxid|32kqe8cbkvdr22')
    if re.findall(pattern=pattern_date, string=content):
        for i in re.findall(pattern=pattern_date, string=content):
            content = re.sub(pattern=pattern_date, string=content, repl='')
    # 第二步：去除受干扰的电话号码
    pattern_phone = re.compile('(\d){11}')
    if pattern_phone:
        content = re.sub(pattern=pattern_phone, string=content, repl='')
    print('第二步：\n', content)

    # 第三步：现在已经对数据进行了分条整理，接下来对厂号和货物进行提取
    changhao_list = re.findall(r'[0-9]+', content)
    print(changhao_list)

    if len(changhao_list) > 1:
        # 长度不为1的
        temp_list = []
        changhao_list_deep = copy.deepcopy(changhao_list)
        for eve_changhao in range(len(changhao_list_deep) - 1, -1, -1):
            # 截取数字后面的数据，并将该字符串从原字符串中去除
            k = content.strip().split(changhao_list_deep[-1])
            content = content.replace(changhao_list_deep[-1] + k[-1], '')
            changhao_list_deep.pop(-1)
            temp_list.append(k[-1])
        for temp_index in range(len(temp_list)):
            if temp_list[temp_index] == ' ':
                temp_list[temp_index] = None
        frame = pd.Series(temp_list, index=changhao_list[::-1])
        new_frame = frame.fillna(method='bfill')
        for u in range(len(changhao_list)):
            item['changhao'] = new_frame.index[u]
            chanpin = new_frame.iloc[u]
            # 对其中的产品数据进行讨论
            for eve_s_index in range(len(chanpin) + 1):
                if chanpin[eve_s_index:eve_s_index + 8] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 8]
                    chanpin = chanpin[:eve_s_index] + '-' * 8 + chanpin[eve_s_index + 8:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 7] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 7]
                    chanpin = chanpin[:eve_s_index] + '-' * 7 + chanpin[eve_s_index + 7:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 6] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 6]
                    chanpin = chanpin[:eve_s_index] + '-' * 6 + chanpin[eve_s_index + 6:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 5] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 5]
                    chanpin = chanpin[:eve_s_index] + '-' * 5 + chanpin[eve_s_index + 5:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 4] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 4]
                    chanpin = chanpin[:eve_s_index] + '-' * 4 + chanpin[eve_s_index + 4:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 3] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 3]
                    chanpin = chanpin[:eve_s_index] + '-' * 3 + chanpin[eve_s_index + 3:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 2] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 2]
                    chanpin = chanpin[:eve_s_index] + '-' * 2 + chanpin[eve_s_index + 2:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                else:
                    pass
    elif len(changhao_list) == 1:
        content = content.strip().split(changhao_list[0])
        new_frame = pd.Series(content[-1], index=changhao_list)
        for u in range(len(changhao_list)):
            item['changhao'] = new_frame.index[u]
            chanpin = new_frame.iloc[u]
            # 对其中的产品数据进行讨论
            for eve_s_index in range(len(chanpin) + 1):
                if chanpin[eve_s_index:eve_s_index + 8] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 8]
                    chanpin = chanpin[:eve_s_index] + '-' * 8 + chanpin[eve_s_index + 8:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 7] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 7]
                    chanpin = chanpin[:eve_s_index] + '-' * 7 + chanpin[eve_s_index + 7:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 6] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 6]
                    chanpin = chanpin[:eve_s_index] + '-' * 6 + chanpin[eve_s_index + 6:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 5] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 5]
                    chanpin = chanpin[:eve_s_index] + '-' * 5 + chanpin[eve_s_index + 5:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 4] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 4]
                    chanpin = chanpin[:eve_s_index] + '-' * 4 + chanpin[eve_s_index + 4:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 3] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 3]
                    chanpin = chanpin[:eve_s_index] + '-' * 3 + chanpin[eve_s_index + 3:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                elif chanpin[eve_s_index:eve_s_index + 2] in products:
                    item['product'] = chanpin[eve_s_index:eve_s_index + 2]
                    chanpin = chanpin[:eve_s_index] + '-' * 2 + chanpin[eve_s_index + 2:]
                    item['cur_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    insert_mysql(item)
                else:
                    pass
    else:
        pass
    print('*' * 100)


# 对contrast_str数据进行遍历
def ergodic_data(item, contrast):
    contrast_str = item['original_content']
    # 对当前的字符串进行分析，根据地名进行切割
    """
        遍历地区列表，把列表中的地区定位到字符串中
    """
    if '切片机' in contrast_str:
        pass
    else:
        if '求购' in contrast_str or '采购' in contrast_str:
            country_index = split_data(area_list, contrast_str)[0]
            # 获取到了每一个分割开来的数据
            new_country_str = split_str(country_index, contrast_str)
            # 获取到了已被分割的数据：形式为--->地名+产品
            # 接下来开始对new_country_str中的数据进行匹配
            t_index = split_data(area_list, contrast_str)[1]
            item['buy_supply'] = '采购'
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
        if '出货' in contrast_str or '出' in contrast_str or "现货" in contrast_str:
            country_index = split_data(area_list, contrast_str)[0]
            # 获取到了每一个分割开来的数据
            new_country_str = split_str(country_index, contrast_str)
            # 获取到了已被分割的数据：形式为--->地名+产品
            # 接下来开始对new_country_str中的数据进行匹配
            t_index = split_data(area_list, contrast_str)[1]
            item['buy_supply'] = '供应'
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
        else:
            item['buy_supply'] = '供应'
            country_index = split_data(area_list, contrast_str)[0]
            # 获取到了每一个分割开来的数据
            new_country_str = split_str(country_index, contrast_str)
            # 获取到了已被分割的数据：形式为--->地名+产品
            # 接下来开始对new_country_str中的数据进行匹配
            t_index = split_data(area_list, contrast_str)[1]

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


def read_html(item, filename):
    fp = open(filename, 'rb')
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

            content_list = i.xpath('.//pre/text()')

            if content_list:
                if len(content_list) > 1:
                    content = ' '.join(content_list)
                    k = re.sub(r':(.*?):', '', emoji.demojize(content)).strip().split('\r\n')
                else:
                    k = re.sub(r':(.*?):', '', emoji.demojize(content_list[0])).strip().split('\r\n')
                # 初步处理之后的字符串
                mid_str = ''.join(k).strip()

                pattern2 = re.compile('\[(.*?)\]')
                content_list = re.sub(pattern2, '', mid_str)
                pattern3 = re.compile('[^\u4e00-\u9fa5a-zA-Z0-9]')
                content1 = re.sub(pattern3, ' ', content_list)
                item['original_content'] = content1
                if len(content1):
                    content2 = content1.replace('。', '').replace('，', ' ').split(' ')
                    content3 = [k for k in content2 if k != '']
                    item['content'] = '，'.join(content3)

                    contrast = item['content'].replace(' ', '')

                    # 对item['contrast']数据进行遍历
                    ergodic_data(item, contrast)
        fp.close()


if __name__ == '__main__':
    db = pymysql.connect(user='root', password='xinqian@saibao', host='10.10.107.7', database='bigdata', port=3306, charset='utf8mb4')
    cursor = db.cursor()

    r_db = redis.Redis(host='127.0.0.1', port=6379, db=1)
    redis_data_dict = 'ods_weixin_update'

    cities = read_mysql_city()
    countries = read_mysql_country()
    provinces = read_mysql_province()

    products = read_mysql_product()
    additional_area = ['澳洲']

    area_list = countries + provinces + cities + additional_area
    # 地区列表
    for eve_area_ in area_list:
        if '省' in eve_area_:
            s = eve_area_.replace('省', '')
            area_list.remove(eve_area_)
            area_list.append(s)
        if '市' in eve_area_:
            s = eve_area_.replace('市', '')
            area_list.remove(eve_area_)
            area_list.append(s)
        if '县' in eve_area_:
            s = eve_area_.replace('县', '')
            area_list.remove(eve_area_)
            area_list.append(s)
    item = {}
    file_dir = './网页格式'
    for root, dir, files in os.walk(file_dir):
        for i in files:
            t = root + '/' + i
            read_html(item, t)
