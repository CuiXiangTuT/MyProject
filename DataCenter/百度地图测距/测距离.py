import os

import requests
import json
from geopy.distance import geodesic
import pandas as pd

AK = "ZOyMfGrlHHFBi0UO64hlG8S2Ws8K8uWX"


def get_excel_data(excel_path):
    columns = ["照片/视频", "拍摄人", "使用水印名称", "拍摄时间", "拍摄地点", "天气", "经度", "纬度", "海拔"]
    excel_data = pd.read_excel(excel_path, skiprows=[0, 1], usecols=[0, 1, 2, 3, 4, 5, 6, 7, 8], names=columns)
    return excel_data


def getPosition(address):
    """

    :param address:
    :return:
    """
    url = r"http://api.map.baidu.com/place/v2/search?query={}&region=全国&output=json&ak={}".format(
        address,
        AK  # 这里是一开始截图用红色圈起来的部分
    )
    res = requests.get(url)
    json_data = json.loads(res.text)

    if json_data['status'] == 0:
        lat = json_data["results"][0]["location"]["lat"]  # 纬度
        lng = json_data["results"][0]["location"]["lng"]  # 经度
    else:
        print("[ERROR] Can not find {}.".format(address))
        return "0,0", json_data["status"]
    return str(lat) + "," + str(lng), json_data["status"]


def calcDistance(loc1, m, n):
    """
    通过拍摄地点确定位置
    :return:
    """
    # coor1 = getPosition(address)[0]  # 经纬度1
    # coor1 = coor1.split(",")
    if "北京" in loc1:
        location_1 = float(n)
        location_2 = float(m)
        coor1 = (location_1, location_2)
        # 鑫汇洋坐标位置
        coor2 = (116.5015004, 39.904630)
        # 这里输入纬度在前，经度在后，所以做一下反转
        distance = geodesic(coor1, coor2[::-1]).m  # 距离(米)
        return distance
    elif "天津" in loc1:
        location_1 = float(n)
        location_2 = float(m)
        coor1 = (location_1, location_2)
        # 鑫汇洋坐标位置
        coor2 = (117.15, 39.11)
        # 这里输入纬度在前，经度在后，所以做一下反转
        distance = geodesic(coor1, coor2[::-1]).m  # 距离(米)
        return distance


if __name__ == '__main__':
    file_dir = "XlSXFile"
    df = pd.DataFrame()
    for root, dir, files in os.walk(file_dir):
        for i in files:
            t = root + '/' + i
            excel_data = get_excel_data(t)
            df = df.append(excel_data, ignore_index=True)
            k = []

            for i in range(len(df)):
                try:
                    distance = calcDistance(df.loc[i]["拍摄地点"], df.loc[i]["经度"], df.loc[i]["纬度"])
                    k.append(distance)
                except:
                    k.append(" ")
            df1 = pd.DataFrame([k], columns=["距离"])
            # df.to_csv('distance3.csv')
            # print('结束')
            print(df)
            print('-' * 50)
