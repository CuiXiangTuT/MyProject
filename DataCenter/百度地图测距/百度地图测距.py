import pandas as pd
import requests
import json
from geopy.distance import geodesic

AK = "ZOyMfGrlHHFBi0UO64hlG8S2Ws8K8uWX"


def getPosition(address):
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


def calcDistance():
    """
    通过拍摄地点确定位置
    :return:
    """
    coor1 = getPosition("天津市·云华里")[0]  # 经纬度1
    coor1 = coor1.split(",")
    location_1 = float(coor1[0])
    location_2 = float(coor1[1])
    coor1 = (location_1, location_2)
    print(coor1)
    coor2 = (117.228763, 39.08166)
    # 这里输入纬度在前，经度在后，所以做一下反转
    distance = geodesic(coor1, coor2[::-1]).m  # 距离(米)
    return distance


if __name__ == '__main__':

    distance = calcDistance()
    print(distance)


