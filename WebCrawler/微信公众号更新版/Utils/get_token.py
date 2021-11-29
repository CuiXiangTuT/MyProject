import json
import random

import requests


def get_token(ip_list):
    """
    因为token会有时效性，需要获取token
    :return: token
    """
    url = 'http://123.57.104.184:7003/auth/login'
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzIwNjY5MzMzNCIsImF1ZCI6IntcImFsbE51bVwiOjAsXCJidXlOdW1cIjowLFwiaWRlbnRpdHlUeXBlXCI6MixcImlzUmVhbFwiOnRydWUsXCJvZmZlckJvb2xlYW5cIjpmYWxzZSxcInBob25lTm9cIjpcIjEzMjA2NjkzMzM0XCIsXCJzdXBwbHlOdW1cIjowLFwic3lzdGVtTXNnQm9vbGVhblwiOnRydWUsXCJzeXN0ZW1Nc2dEYXRlU3RyXCI6XCIyMDIxLTA5LTA5XCIsXCJ1aWRcIjpcIjcyYTc2N2NhNDE1MTQyYzliMzgzYjY1ZmEzMThiYzI1XCIsXCJ1c2VySWRcIjpcIjg2OTU0NDg4NFwiLFwidXNlck5hbWVcIjpcIjcuQU5HXCJ9IiwiZXhwIjoxNjMxODQwOTAzLCJpYXQiOjE2MzEyMzYxMDN9.vd_mqjsMn4hDCZ3o9Wd-ASvE6YKaSEHBVDFlNgZYOe723JmURtclobS7OhbN-BCZKF2gfPosWbarkFJYZrJmjg',
        'Connection': 'keep-alive',
        'Content-Length': '129',
        'Content-Type': 'application/json',
        'Cookie': 'rememberMe=gnPPWQ5sU+5Cv9L70s/cmDvjBpD/l9ieJMVfP5025mpiOdYo7OmoauifDTKj+YGdJdUFTccpTEqEWqW2kHGUaipHjtVlboz1i7RLUTGRnO3cvEMAuwUyU9tdlvjXHWYCtQilRU5SqUYQs0q07qSVNykvJA5CnxSzctshfBn839qYX9RWw1sesHujlJigssDDgaSvMRkFSQ78tz/TtaiItAhVEfDw+XLk9CFrInxkZOrNn7kzwYTXLIEo4R5dBvVwQLddUZlPsHzJQWO1qiSFzS0WPkPVSkEBv2U9n0gRiApaKrPQMQ14InUnCmKThOf5UrzUpQLH+v6NmVc2k8HgxlR9+OUSI6JTVNIpRN8/Vialqthk9U4BaKrK69KPKSq3MPGmScEzByyk/lhieEAhIdnJiKol6lg1pTcmZYAUHsWQCfnANExM+hGLkK8IOiqBtekIIeTUu1Zgv2uaSB+5mhI5SPNB+ZKaOoM311k37JkWZxhjufsVZ7NCocJPBj6fTmorbRUsChAjjTAvpuvenu28XQD8g3FwbcF0RQneRoB0Dj2fLEUnsoJCDfVLBrqplwg/DqPO7Wled+AB5YwhN5xbAvq21iokDB2tuh0mjKbjh1rRlJd7TVhcJpy1EMu9Gut5fs7/CmKg6525rsI8MMALm3Nyd+Q7Bw8iCa/1yUDPVItxCbcdVaVQJpS2HDRslvl2lQCEtmTClHSMu4pUZrJuMfeHeg74Hj2MSro9op8bX3l9eTsFoLYiKAMAGo1GfjYbqoMqaVOhRq5ZHHJG+3vrf+9s59SxBIz0RQ4rqJhEYgAKBy/s8KroClSh5mcWUeclXh/8ZKXZQzBnemsNuJyXqHldu6CqKXHbR2SuvUGG+9Fd4Cyh9UyBbH6hzbHP0/fG7dgTqooijNLZG2a+5SHwo7PVnz+YpM7RnXqu/yBFev2LWoqK24fLzJuLCiIaN/GMz8ipUCuWVaxbVhqIirndeEkDtzgpN0g8tqWQItTRXduxLi8v2BJWHI+9iFfhTiKtdkFSvY4EOkeBLQzFuVR311/KbisS+rPKiiakRKF2i8v8FzY6/lEeg4rrSh1xVJG3kpylXziLCTfNJS9gLwQkSchcL2b5CF+LU+VfPMKTgYuUdCBC3rA+Clwk76wQ; saibaoCookieadmin=709c2ae7-e8a9-4482-bc06-b1038278edc2',
        'Host': '123.57.104.184:7003',
        'Origin': 'http://123.57.104.184:7003',
        'Referer': 'http://123.57.104.184:7003/doc.html',
        'Request-Origion': 'SwaggerBootstrapUi',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        "appCode": "",
        "code": "",
        "codeId": 0,
        "isNewUser": True,
        "loginName": "13037639858",
        "password": "123456",
        "type": 1
    }
    ip = random.choice(ip_list)
    token = requests.post(url=url, headers=headers, data=json.dumps(data),
                          proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()["data"]["token"]
    return token
