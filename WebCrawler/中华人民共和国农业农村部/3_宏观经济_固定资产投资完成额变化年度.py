import random
from datetime import datetime

import requests
import redis
import pymysql

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
# 固定资产投资完成额变化
redis_dict_key = 'ods_cnncnybgdzctzwcebhnd'


# 获取讯代理IP
def getIp():
    xdl_url = 'http://api.xdaili.cn/xdaili-api//greatRecharge/getGreatIp?spiderId=913d4f4b67e24be0998a3eb344ff732b&orderno=YZ2021923652gUFZCj&returnType=2&count=10'
    ipListData = requests.get(url=xdl_url).json()
    ipList = []
    ipList.clear()
    # 将ip以字典的形式添加至ip池
    for everyIp in ipListData['RESULT']:
        ipList.append({
            'ip': everyIp['ip'],
            'port': everyIp['port']
        })
    return ipList


def insertMysql(item):
    if redisDB.hexists(redis_dict_key, item['completedAmountofSocialInvestment'] + '-' + item['Ctime'] + '-' + item[
        'nlmyCompletionAmount']):
        print('已存在该值，不作处理...')
    else:
        redisDB.hset(redis_dict_key, item['completedAmountofSocialInvestment'] + '-' + item['Ctime'] + '-' + item[
            'nlmyCompletionAmount'], 0)
        sql = 'insert into ods_chinanongcunnongyebugdzctzwcebhnd(classification,completedAmountofSocialInvestment,Ctime,nlmyCompletionAmount,nlmyProportion,unit,insertTime)values (%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (item['classification'],
                             item['completedAmountofSocialInvestment'], item['Ctime'], item['nlmyCompletionAmount'],
                             item['nlmyProportion'], item['unit'], item['insertTime']))
        print('正在插入数据，请稍等...')
        conn.commit()


def getData():
    url = 'http://zdscxx.moa.gov.cn:8080/nyb/qggdzctz'
    item = {}
    headers = {
        'Referer': 'http://zdscxx.moa.gov.cn:8080/nyb/pc/index.jsp',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    data = {
        'item': '年度'
    }
    ip = random.choice(ipList)
    response = requests.post(url=url, headers=headers, data=data,
                             proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['result']['rowDatas']
    item['classification'] = '年度'
    for perData in response:
        # 全社会固定资产投资完成额
        item['completedAmountofSocialInvestment'] = perData['全社会固定资产投资完成额']
        # 时间
        item['Ctime'] = perData['时间']
        try:
            # 农、林、牧、渔业全社会固定资产投资完成额
            item['nlmyCompletionAmount'] = perData['农、林、牧、渔业全社会固定资产投资完成额']
        except:
            item['nlmyCompletionAmount'] = ''
        try:
            # 农、林、牧、渔业投资占比(%)
            item['nlmyProportion'] = perData['农、林、牧、渔业投资占比(%)']
        except:
            item['nlmyProportion'] = ''
        # 单位
        item['unit'] = '亿元'
        # 插入时间
        item['insertTime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insertMysql(item)


if __name__ == '__main__':
    ipList = getIp()
    getData()
    cursor.close()
    conn.close()
