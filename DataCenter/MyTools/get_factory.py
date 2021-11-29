import re
import pandas as pd
import pymysql


def get_factory_data():
    """
    获取厂号及国家
    :return:
    """
    mysql_cn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc",
                               port=3306)
    factory_data = pd.read_sql("select * from ods_comm_factory", con=mysql_cn)
    # factory_list = [x for x in list(factory_data["factory_no"]) if
    #                 '-' not in x[0]]
    # print(factory_list)
    data = {
        "factory_no": list(factory_data["factory_no"]),
        "country_name": list(factory_data["country_name"])
    }
    df = pd.DataFrame(data)
    df["short_hand"] = [re.sub('[a-zA-Z]', '', x) for x in factory_data["factory_no"]]
    print(df)
    # new_factory_list = [re.sub('[a-zA-Z]', '', x) for x in factory_list]
    # total_factory_no = list(set(factory_list+new_factory_list))
    # return total_factory_no


if __name__ == '__main__':
    get_factory_data()
