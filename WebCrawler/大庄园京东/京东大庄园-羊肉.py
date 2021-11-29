import datetime
import time
from pprint import pprint
import pymysql
import redis
import requests
from lxml import etree

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=2)
redis_dict_key = 'ods_jingdong_dazhuangyuanyangrou'


def splitStr(l):
    print(l)
    item['tradeName'] = ''
    item['itemNumber'] = ''
    item['grossWeightOfGoods'] = ''
    item['commodityOrigin'] = ''
    item['category'] = ''
    item['packingForm'] = ''
    item['feedingMode'] = ''
    item['countryOfOrigin'] = ''
    item['varieties'] = ''
    item['cookingAdvice'] = ''
    item['weight'] = ''
    item['saveStatus'] = ''
    item['importAndExport'] = ''
    for s in l:
        if '商品名称' in s:
            item['tradeName'] = s[5:]
        elif '商品编号' in s:
            item['itemNumber'] = s[5:]
        elif '商品毛重' in s:
            item['grossWeightOfGoods'] = s[5:]
        elif '商品产地' in s:
            item['commodityOrigin'] = s[5:]
        elif '类别' in s:
            item['category'] = s[3:]
        elif '包装形式' in s:
            item['packingForm'] = s[5:]
        elif '饲养方式' in s:
            item['feedingMode'] = s[5:]
        elif '原产地' in s:
            item['countryOfOrigin'] = s[4:]
        elif '类别' in s:
            item['varieties'] = s[3:]
        elif '烹饪建议' in s:
            item['cookingAdvice'] = s[5:]
        elif '重量' in s:
            item['weight'] = s[3:]
        elif '保存状态' in s:
            item['saveStatus'] = s[5:]
        elif '国产/进口' in s:
            item['importAndExport'] = s[6:]
    item['insertTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item['meatSort'] = '羊肉'
    time.sleep(0.5)
    insertMysql(item)
    pprint(item)
    print('-' * 50)


def insertMysql(item):
    if redisDB.hexists(redis_dict_key, item['title'] + '-' + str(item['price'])):
        print('数据库已有该数据，不做处理~~~')
    else:
        redisDB.hset(redis_dict_key, item['title'] + '-' + str(item['price']), 0)
        sql = 'insert into ods_jd_dazhuangyuan(title,meatSort,price,brand,tradeName,itemNumber,grossWeightOfGoods,commodityOrigin,category,packingForm,feedingMode,countryOfOrigin,varieties,cookingAdvice,weight,saveStatus,importAndExport,insertTime)values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql, (
            item['title'], item['meatSort'], item['price'], item['brand'], item['tradeName'], item['itemNumber'],
            item['grossWeightOfGoods'],
            item['commodityOrigin'], item['category'], item['packingForm'], item['feedingMode'],
            item['countryOfOrigin'],
            item['varieties'], item['cookingAdvice'], item['weight'], item['saveStatus'], item['importAndExport'],
            item['insertTime']))
        print('数据正在插入，请稍等...')
        conn.commit()


def getData(res):
    """
    获取详情页的url
    :param res:
    :return:
    """
    response = etree.HTML(res)
    liList = response.xpath('.//li[@class="gl-item"]/div')
    for perLi in liList:
        detailUrl = 'https:' + perLi.xpath('.//div[@class="p-img"]/a/@href')[0]
        headers = {
            'authority': 'item.jd.com',
            'method': 'GET',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '__jdu=34820952; shshshfpa=4422ac4e-aae1-bac1-bf5c-7582e3897c2d-1627269659; shshshfpb=dSymlNuOXQ65rxqybfxoFYg%3D%3D; areaId=0; PCSYCityID=CN_0_0_0; ipLoc-djd=1-72-55653-0; user-key=5dccd210-4b6f-4e30-9e8b-d651c7b6b163; unpl=V2_ZzNtbRZeSxBxCkIDexhaDGJXFVgSURESJgxCB3seXlVgABdUclRCFnUURlVnGFQUZgsZWERcQxNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHkcVQZmCxZecmdEJUU4QVN5GVkBVwIiXHIVF0lzC0JUfRoRB2IKEVxKU0AldDhF; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e894535f10784e64a7c6b55b163a6248|1633744037873; __jdc=122270672; shshshfp=b38a19b2564624749fd6ebae699a8a78; __jda=122270672.34820952.1626255775.1633742145.1633750611.17; token=622492968c9920c94e22cc9fe69a01ca,2,907639; __tk=JvnElsG0jUnEJsjEIvkilvtzkct0kzSxjcuoIiupkUn,2,907639; shshshsID=2fec954946f2807502456e8b7731d331_5_1633751990365; __jdb=122270672.5.34820952|17.1633750611; 3AB9D23F7A4B3C9B=TA5KAGBNRD4YFUGMDQST52VGH7TGFLYX4UPWD3PBZYB2RBC7IUGG7EUKU3GHBM4ZGFJ73VLDAY3QYIUCY6MY3BGEEU',
            'referer': 'https://search.jd.com/',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
        }
        # 产品
        item['title'] = ' '.join(perLi.xpath('.//div[contains(@class,"p-name")]/a/em//text()')).replace('\t\n', '')
        # 价格
        item['price'] = perLi.xpath('.//div[@class="p-price"]/strong//i/text()')[0]
        detailResponse = requests.get(url=detailUrl, headers=headers).text
        kresponse = etree.HTML(detailResponse)
        dataList = kresponse.xpath('.//ul[contains(@class,"parameter2") and contains(@class,"p-parameter-list")]//li//text()')

        try:
            # 品牌
            item['brand'] = kresponse.xpath('.//ul[@class="p-parameter-list"]/li/a/text()')[0]
        except:
            item['brand'] = ''
        splitStr(dataList)


def getFrontData():
    """
    获取前30条数据
    :return:
    """
    url = 'https://search.jd.com/search?'
    headers = {
        'authority': 'search.jd.com',
        'method': 'GET',
        'path': '/search?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&qrst=1&stock=1&stock=1&ev=exbrand_%E5%A4%A7%E5%BA%84%E5%9B%AD%EF%BC%88Grand%20Farm%EF%BC%89%5E&cid3=13583',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '__jdu=34820952; shshshfpa=4422ac4e-aae1-bac1-bf5c-7582e3897c2d-1627269659; shshshfpb=dSymlNuOXQ65rxqybfxoFYg%3D%3D; qrsc=3; areaId=0; PCSYCityID=CN_0_0_0; rkv=1.0; ipLoc-djd=1-72-55653-0; user-key=5dccd210-4b6f-4e30-9e8b-d651c7b6b163; unpl=V2_ZzNtbRZeSxBxCkIDexhaDGJXFVgSURESJgxCB3seXlVgABdUclRCFnUURlVnGFQUZgsZWERcQxNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHkcVQZmCxZecmdEJUU4QVN5GVkBVwIiXHIVF0lzC0JUfRoRB2IKEVxKU0AldDhF; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e894535f10784e64a7c6b55b163a6248|1633744037873; __jda=122270672.34820952.1626255775.1633677784.1633742145.16; __jdc=122270672; shshshfp=b38a19b2564624749fd6ebae699a8a78; token=61c225f11e8ed404e02f746ae87e1088,2,907637; __tk=qAtsrAG52wgYrUV3qwPu2wNsKUytrDbY2wNtqUbuqDqD2uSAqcSE2V,2,907637; __jdb=122270672.176.34820952|16.1633742145; shshshsID=c63db76be42b4fcbf015ac2aa33f4713_176_1633748362205; 3AB9D23F7A4B3C9B=TA5KAGBNRD4YFUGMDQST52VGH7TGFLYX4UPWD3PBZYB2RBC7IUGG7EUKU3GHBM4ZGFJ73VLDAY3QYIUCY6MY3BGEEU',
        'referer': 'https://search.jd.com/Search?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&enc=utf-8&pvid=84b043a08a634d8099790c89ee57b77b',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
    }
    data = {
        'keyword': '大庄园',
        'qrst': '1',
        'stock': '1',
        'ev': 'exbrand_大庄园（Grand Farm）^',
        'cid3': '13583',
    }
    res = requests.get(url=url, headers=headers, params=data).text
    getData(res)


def getBackData():
    """
    获取后30条数据
    :return:
    """
    url = 'https://search.jd.com/s_new.php?'
    headers = {
        'authority': 'search.jd.com',
        'method': 'GET',
        'path': '/s_new.php?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&qrst=1&stock=1&ev=exbrand_%E5%A4%A7%E5%BA%84%E5%9B%AD%EF%BC%88Grand%20Farm%EF%BC%89%5E&pvid=7b3cabd03cd94f46a524b231d43d3048&cid3=13583&cid2=13581&page=2&s=31&scrolling=y&log_id=1633748391916.5072&tpl=1_M&isList=0&show_items=100007732554,4741825,100016604492,100011411056,100011848444,100011411058,100005889082,100012339846,100006586145,100006524503,69815915358,100006586143,100017923018,100009556025,100016753380,100025623390,69898983857,69803414180,100016161658,69801012323,100009556013,69802477194,69653477306,69968216686,69968216687,10021072017303,69968852591,69803414181,69889418249,69815915359',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': '__jdu=34820952; shshshfpa=4422ac4e-aae1-bac1-bf5c-7582e3897c2d-1627269659; shshshfpb=dSymlNuOXQ65rxqybfxoFYg%3D%3D; qrsc=3; areaId=0; PCSYCityID=CN_0_0_0; rkv=1.0; ipLoc-djd=1-72-55653-0; user-key=5dccd210-4b6f-4e30-9e8b-d651c7b6b163; unpl=V2_ZzNtbRZeSxBxCkIDexhaDGJXFVgSURESJgxCB3seXlVgABdUclRCFnUURlVnGFQUZgsZWERcQxNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHkcVQZmCxZecmdEJUU4QVN5GVkBVwIiXHIVF0lzC0JUfRoRB2IKEVxKU0AldDhF; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e894535f10784e64a7c6b55b163a6248|1633744037873; __jda=122270672.34820952.1626255775.1633677784.1633742145.16; __jdc=122270672; shshshfp=b38a19b2564624749fd6ebae699a8a78; token=61c225f11e8ed404e02f746ae87e1088,2,907637; __tk=qAtsrAG52wgYrUV3qwPu2wNsKUytrDbY2wNtqUbuqDqD2uSAqcSE2V,2,907637; __jdb=122270672.177.34820952|16.1633742145; shshshsID=c63db76be42b4fcbf015ac2aa33f4713_177_1633748392692; 3AB9D23F7A4B3C9B=TA5KAGBNRD4YFUGMDQST52VGH7TGFLYX4UPWD3PBZYB2RBC7IUGG7EUKU3GHBM4ZGFJ73VLDAY3QYIUCY6MY3BGEEU',
        'referer': 'https://search.jd.com/search?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&qrst=1&stock=1&ev=exbrand_%E5%A4%A7%E5%BA%84%E5%9B%AD%EF%BC%88Grand%20Farm%EF%BC%89%5E&cid3=13583',
        'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': "Windows",
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'keyword': '大庄园',
        'qrst': '1',
        'stock': '1',
        'ev': 'exbrand_大庄园（Grand Farm）^',
        'pvid': '7b3cabd03cd94f46a524b231d43d3048',
        'cid3': '13583',
        'cid2': '13581',
        'page': '2',
        's': '31',
        'scrolling': 'y',
        'log_id': '1633748391916.5072',
        'tpl': '1_M',
        'isList': '0',
        'show_items': '100007732554,4741825,100016604492,100011411056,100011848444,100011411058,100005889082,100012339846,100006586145,100006524503,69815915358,100006586143,100017923018,100009556025,100016753380,100025623390,69898983857,69803414180,100016161658,69801012323,100009556013,69802477194,69653477306,69968216686,69968216687,10021072017303,69968852591,69803414181,69889418249,69815915359',
    }
    res = requests.get(url=url, headers=headers, params=data).text
    getData(res)


if __name__ == '__main__':
    item = {}
    getFrontData()
    time.sleep(2)
    getBackData()
    cursor.close()
    conn.close()
