import json

import requests

url = 'https://appapi.cnhnb.com/esearch-poly/api/transform/supply/v509/list'
headers = {
'Host':'appapi.cnhnb.com',
'Connection':'keep-alive',
'Content-Length':'67',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
'X-B3-TRACEID':'0KTUTN8TMDXOW2TJ',
'X-CLIENT-APPID':'2',
'X-CLIENT-ID':'e2932c8-74a9-588c-ae80-0d1a86975',
'X-CLIENT-NONCE':'d096a97f0b03e8b786ac5539f5eed69a',
'X-CLIENT-PAGE':'subPages/supply/supply-search/index',
'X-CLIENT-SID':'S_0KTUTN8TMDXOW2TJ',
'X-CLIENT-SIGN':'1f36b7706782255106d20c2b57f2f8609e53e2fbab9c56ee5960e4cadf1df0985e49dfcef097e10d7d19f830133f8912',
'X-CLIENT-TICKET':'',
'X-CLIENT-TIME':'1632273748330',
'X-CLIENT-UA':'',
'X-HN-JOB':'If you see these message, I hope you dont hack us, I hope you can join us! Please visit https://www.cnhnkj.com/job.html',
'access-token':'368172066AC24A299FA4118A94555435',
'content-type':'application/json',
'hn-app-id':'xapp',
'osType':'xapp',
'Referer':'https://servicewechat.com/wx6e72282bcc43a3c5/137/page-frame.html',
'Accept-Encoding':'gzip, deflate, br',
}
data = {
  "pageNumber": 1,
  "pageSize": 10,
  "cateId3": 2001111,
  "keyword": "牛肉"
}
res = requests.post(url=url,headers=headers,json=json.dumps(data)).json()
print(res)