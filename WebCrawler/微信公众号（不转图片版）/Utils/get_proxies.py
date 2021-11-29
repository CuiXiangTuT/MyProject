import time

import requests


def get_ip_list():
    """
    获取代理ip
    :return: 代理IP列表
    """
    xdl_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=913d4f4b67e24be0998a3eb344ff732b&orderno=YZ2021923652gUFZCj&returnType=2&count=5'
    # xdl_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=193f9bddb3fe4dd9bc98ef673f3f9cb9&orderno=YZ202111108996Js59kF&returnType=2&count=10'
    time.sleep(2)
    ip_list_data = requests.get(url=xdl_url).json()
    ip_list = []
    ip_list.clear()
    # 将ip以字典的形式添加至ip池
    for everyIp in ip_list_data['RESULT']:
        ip_list.append({
            'ip': everyIp['ip'],
            'port': everyIp['port']
        })

    return ip_list
