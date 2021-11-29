import pymysql
import pandas as pd


def get_product_list():
    """
    获取品类表
    :return: 品类、父级id
    """
    mysql_cn = pymysql.Connect(user="bigdata2021", password="bigdata@2021##", host="8.140.151.237", database="bigdata",
                               port=3306)
    product_list = pd.read_sql('select * from d_supply_product_class;', con=mysql_cn)
    return product_list["class_name"][2:], product_list["pid"][2:]


def get_country_list():
    """
    获取国家表
    :return: 国家简称
    """
    mysql_cn = pymysql.Connect(user="bigdata2021", password="bigdata@2021##", host="8.140.151.237", database="bigdata",
                               port=3306)
    country_list = pd.read_sql('select * from d_country;', con=mysql_cn)
    return country_list["id"], country_list["name"]


def get_province_list():
    """
    获取国内省表
    :return: 省份简称
    """
    mysql_cn = pymysql.Connect(user="bigdata2021", password="bigdata@2021##", host="8.140.151.237", database="bigdata",
                               port=3306)
    province_list = pd.read_sql('select * from d_bs_province;', con=mysql_cn)
    return province_list["SHORT_NAME"]


def get_city_list():
    """
    获取城市表
    :return: 城市简称
    """
    mysql_cn = pymysql.Connect(user="bigdata2021", password="bigdata@2021##", host="8.140.151.237", database="bigdata",
                               port=3306)
    city_list = pd.read_sql('select * from d_bs_city;', con=mysql_cn)
    return city_list["SHORT_NAME"]


def get_plant_list():
    """
    获取厂号表
    :return: 工厂代号、国家编号、类型
    """
    mysql_cn = pymysql.Connect(user="bigdata2021", password="bigdata@2021##", host="8.140.151.237", database="bigdata",
                               port=3306)
    city_list = pd.read_sql('select * from d_bs_plant;', con=mysql_cn)
    return city_list["plant_name"], city_list["plant_country_no"], city_list["type"]


def merge_country_plant():
    """
    合并国家表与工厂表
    :return: 国家与工厂的合并表，类型dataframe
    """
    plant_name, plant_country_no, plant_type = get_plant_list()
    country_id, country_name = get_country_list()
    plant_country_no = map(lambda x: int(x), plant_country_no)
    data1 = {"plant_name": plant_name, "plant_country_no": plant_country_no, "plant_type": plant_type}
    df1 = pd.DataFrame(data=data1)
    data2 = {"plant_country_no": country_id, "country_name": country_name}
    df2 = pd.DataFrame(data=data2)
    result = df1.merge(df2, how="inner", on="plant_country_no")
    return result


def merge_product_productSort():
    """
    合并产品和产品类别表
    :return: 产品、产品pid、大类
    """
    class_name, class_pid = get_product_list()
    data1 = {"class_name": class_name, "class_pid": class_pid}
    df1 = pd.DataFrame(data=data1)
    data2 = {"class_pid": [1, 2], "main_class_name": ["牛", "羊"]}
    df2 = pd.DataFrame(data=data2)
    result = df1.merge(df2, how="inner", on="class_pid")
    return result


def total_class_sort():
    """
    获取所有的厂号、产品、大类、城市、省份、国家
    :return:
    """
    # 厂号表
    plant_name, plant_country_no, plant_type = get_plant_list()
    # 国家表
    country_id, country_name = get_country_list()
    # 城市表
    city_list = get_city_list()
    # 产品表
    class_name, class_pis = get_product_list()
    # 省份表
    province_list = get_province_list()
    total_list = plant_name.tolist() + country_name.tolist() + city_list.tolist() + class_name.tolist() + province_list.tolist() + [
        "牛肉", "羊肉"]
    return total_list
