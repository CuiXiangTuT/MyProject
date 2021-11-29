import datetime
import pymysql
import redis
import requests

# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc-ods", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=3)
redis_dict_key = 'ods_bifu_hangqingzoushi_niurou_xianhuo'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, item['key_word'] + '-' + str(item['price'])):
        print('该数据已入库，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key, item['key_word'] + '-' + str(item['price']), 0)
        sql = 'insert into ods_bifu_hangqingzoushi_niurou(sort_trend,feeding_mode,country,part,create_date,key_word,growth_rate,price,insert_time)values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item["sort_trend"], item["feeding_mode"], item["country"], item["part"], item["create_date"],
            item["key_word"],
            item["growth_rate"], item["price"], item["insert_time"]))
        conn.commit()
        print('该数据正在插入，稍等~~~')


def get_price_data(dict_data):
    """
    获取历史日期数据
    :param dict_data: 传入进来一个字典类型的数据
    :return:
    """
    item = dict()
    url = "https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceDataIndex"
    headers = {
        'referer': 'http://www.beeftochina.cn/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
        'x-token': 'ea27f587-d073-4186-9d55-a42c21530863',
    }
    json_data = {"MessageID": "8cdbc7d6-4794-4a33-adb7-663425a1e405", "MessageType": 3000000004,
                 "Data": {"UserID": "danaodaiyangyang", "Part": dict_data["part"], "Country": dict_data["country"],
                          "Parts": [dict_data["part"]],
                          "Countries": [dict_data["country"]], "RecommendDay": 0,
                          "FeedingMode": dict_data["feeding_mode"], "Type": "_spotgoods",
                          "IsFirst": True, "IsEn": False}}
    rows_list = requests.post(url=url, headers=headers, json=json_data).json()["Data"]["Row"]
    # 日期表
    categories_list = rows_list["categories"]
    # 增长率表
    rise_list = rows_list["riseList"][0]
    # 价格表
    series_list = rows_list["series"][0]["data"]
    # 将数据进行打包
    zip_list = list(zip(categories_list, rise_list, series_list))
    # 谷饲、草饲
    item["feeding_mode"] = dict_data["feeding_mode"]
    # 国家
    item["country"] = dict_data["country"]
    # 部位
    item["part"] = dict_data["part"]
    # 大类
    item["sort_trend"] = "牛肉"
    for per_data in zip_list:
        # 日期
        item["create_date"] = per_data[0]
        # 关键字
        item["key_word"] = per_data[1]["key"]
        # 增长率
        item["growth_rate"] = per_data[1]["rise"]
        # 价格
        item["price"] = per_data[2]
        # 插入日期
        item["insert_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(item)
        insert_mysql(item)


def get_country_part():
    """
    获取行情走势-牛肉-现货
    :return:
    """
    feeding_mode_list = ["草饲", "谷饲"]
    for feeding_mode in feeding_mode_list:
        country_part = dict()
        url = "https://www.beeftochina.com.cn/api/SystemApi/GetWebPriceDataList"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
        }
        json_data = {"MessageID": "7d7f9dc1-a398-4a2b-93cb-d623ebc6ef51", "MessageType": 3000000001,
                     "Data": {"UserID": "danaodaiyangyang", "ReportID": 1846, "PreReportID": 1839, "OriginPlace": "全部",
                              "Part": "全部", "FeedingMode": feeding_mode}}
        rows_list = requests.post(url=url, headers=headers, json=json_data).json()["Data"]["Rows"]
        for row in rows_list:
            # 饲养方式
            country_part["feeding_mode"] = row["FeedingMode"]
            # 国家
            country_part["country"] = row["OriginPlace"]
            # 部位
            country_part["part"] = row["Part"]
            get_price_data(country_part)


if __name__ == '__main__':
    get_country_part()
