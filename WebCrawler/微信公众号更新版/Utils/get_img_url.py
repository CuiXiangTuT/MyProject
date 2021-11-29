import random

import requests


def get_img_url(token, file_path, img_name, ip_list):
    """
    返回图片的url
    :param token: token
    :param file_path: 文件路径
    :param img_name: 图片名
    :param ip: 代理ip
    :return: 图片的新url
    """
    url = 'http://123.57.104.184:7003/upload/picture'

    headers = {
        'Referer': 'http://123.57.104.184:7003/doc.html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
        "Authorization": token
    }

    data = {
        'file': '(binary)',
        'Authorization': token,
        'app_code': '',
        'version': '',
    }
    ip = random.choice(ip_list)
    files = {'file': open('./imgFile/' + file_path + '/' + img_name + '.png', 'rb')}
    img_url = requests.post(url=url, headers=headers, data=data, files=files,
                            proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['data']['path']
    return img_url
