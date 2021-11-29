import json
import time

import requests

url = "https://pcapi.cnhnb.com/communication/api/auth/im/operate/call"

headers = {
    'authority': 'pcapi.cnhnb.com',
    'method': 'POST',
    # 'path': '/communication/api/auth/im/operate/call',
    'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-length': '77',
    'content-type': 'application/json',
    'origin': 'https://www.cnhnb.com',
    'referer': 'https://www.cnhnb.com/',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
    'x-b3-traceid': '0KWA15YIEXZ8JC0O',
    'x-client-appid': '4',
    'x-client-id': '0df4d4c-6480-49bf-8780-1b067f235',
    'x-client-nonce': '0a9578fb38edb8d4cda717ca3269cd05',
    'x-client-page': '/gongying/6236023/',
    'x-client-sid': 'S_0KWA37119VDRQ1F9',
    'x-client-sign': 'f998d0eecd4a66720d66ee190dc4ac492742bbaadf9cdf1d38a052efa8eef805a36aa782f6f2932f6adf17169c62becd',
    'x-client-ticket': '8468fd4c-c852-4667-a91a-ec43809a192c',
    'x-client-time': str(int(time.time()*1000)),
    'x-hn-job': 'If you see these message, I hope you dont hack us, I hope you can join us! Please visit https://www.cnhnkj.com/job.html',
}

data = {"toHnUserId": 760867764, "businessType": 1, "sourceFrom": 2, "businessId": 6236023}
response = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
print(response)