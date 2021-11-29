import datetime
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
redis_dict_key = 'ods_jingdong_dazhuangyuanniurou'


def splitStr(l):
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
        elif '品种' in s:
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
    item['meatSort'] = '牛肉'
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
            'path': str(perLi.xpath('.//div[@class="p-img"]/a/@href')[0]),
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '__jdu=34820952; shshshfpa=4422ac4e-aae1-bac1-bf5c-7582e3897c2d-1627269659; shshshfpb=dSymlNuOXQ65rxqybfxoFYg%3D%3D; areaId=0; PCSYCityID=CN_0_0_0; ipLoc-djd=1-72-55653-0; user-key=5dccd210-4b6f-4e30-9e8b-d651c7b6b163; unpl=V2_ZzNtbRZeSxBxCkIDexhaDGJXFVgSURESJgxCB3seXlVgABdUclRCFnUURlVnGFQUZgsZWERcQxNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHkcVQZmCxZecmdEJUU4QVN5GVkBVwIiXHIVF0lzC0JUfRoRB2IKEVxKU0AldDhF; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e894535f10784e64a7c6b55b163a6248|1633744037873; __jdc=122270672; shshshfp=b38a19b2564624749fd6ebae699a8a78; __jda=122270672.34820952.1626255775.1633742145.1633750611.17; token=622492968c9920c94e22cc9fe69a01ca,2,907639; __tk=JvnElsG0jUnEJsjEIvkilvtzkct0kzSxjcuoIiupkUn,2,907639; shshshsID=2fec954946f2807502456e8b7731d331_5_1633751990365; __jdb=122270672.5.34820952|17.1633750611; 3AB9D23F7A4B3C9B=TA5KAGBNRD4YFUGMDQST52VGH7TGFLYX4UPWD3PBZYB2RBC7IUGG7EUKU3GHBM4ZGFJ73VLDAY3QYIUCY6MY3BGEEU',
            'referer': 'https://item.jd.com/html/token.html?returnUrl={}'.format(detailUrl),
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
        response = etree.HTML(detailResponse)
        dataList = response.xpath(
            './/ul[contains(@class,"parameter2") and contains(@class,"p-parameter-list")]//li/text()')

        try:
            # 品牌
            item['brand'] = response.xpath('.//ul[@class="p-parameter-list"]/li/a/text()')[0]
        except:
            item['brand'] = ''
        splitStr(dataList)


def getFrontData():
    """
    获取前30条数据
    :return:
    """
    url = 'https://search.jd.com/search?'
    pageList = [1, 3]
    sList = [1, 61]
    zipList = list(zip(pageList, sList))
    for perZip in zipList:
        headers = {
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/search?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&qrst=1&suggest=1.his.0.0&wq=%E5%A4%A7%E5%BA%84%E5%9B%AD&stock=1&ev=exbrand_%E5%A4%A7%E5%BA%84%E5%9B%AD%EF%BC%88Grand%20Farm%EF%BC%89%5E&pvid=e9401337a3714baa84c1ca1d58856c3c&cid3=13582&cid2=13581&page=3&s=61&click=0',
            'scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': '__jdu=34820952; shshshfpa=4422ac4e-aae1-bac1-bf5c-7582e3897c2d-1627269659; shshshfpb=dSymlNuOXQ65rxqybfxoFYg%3D%3D; qrsc=3; areaId=0; PCSYCityID=CN_0_0_0; rkv=1.0; ipLoc-djd=1-72-55653-0; user-key=5dccd210-4b6f-4e30-9e8b-d651c7b6b163; unpl=V2_ZzNtbRZeSxBxCkIDexhaDGJXFVgSURESJgxCB3seXlVgABdUclRCFnUURlVnGFQUZgsZWERcQxNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHkcVQZmCxZecmdEJUU4QVN5GVkBVwIiXHIVF0lzC0JUfRoRB2IKEVxKU0AldDhF; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e894535f10784e64a7c6b55b163a6248|1633744037873; __jdc=122270672; shshshfp=b38a19b2564624749fd6ebae699a8a78; __jda=122270672.34820952.1626255775.1633756072.1633762929.19; __jdb=122270672.11.34820952|19.1633762929; shshshsID=94744ab6bdb6f87cbb49f0856960a44f_11_1633765304530; 3AB9D23F7A4B3C9B=TA5KAGBNRD4YFUGMDQST52VGH7TGFLYX4UPWD3PBZYB2RBC7IUGG7EUKU3GHBM4ZGFJ73VLDAY3QYIUCY6MY3BGEEU',
            'referer': 'https://search.jd.com/Search?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&enc=utf-8&suggest=1.his.0.0&wq=&pvid=87a7ee7422f947e3bc8cc15e891a791c',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
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
            'suggest': '1.his.0.0',
            'wq': '大庄园',
            'stock': '1',
            'ev': 'exbrand_大庄园（Grand Farm）^',
            'pvid': 'e9401337a3714baa84c1ca1d58856c3c',
            'cid3': '13582',
            'cid2': '13581',
            'page': str(perZip[0]),
            's': str(perZip[1]),
            'click': '0',
        }
        res = requests.get(url=url, headers=headers, params=data).text
        getData(res)


def getBackData():
    """
    获取后30条数据
    :return:
    """
    url = 'https://search.jd.com/s_new.php?'
    pageList = [2, 4]
    sList = [31, 91]
    itemsList = [
        '100005224206,100006306997,4326110,100011531288,100011531272,100011411060,8543963,69804863390,100025093420,100006535417,100012406542,100017163686,69802774693,100012406562,100018208748,69807340201,69801326059,69768151285,10031413109896,100009828453,100012406520,100010273221,100010273211,100018175356,69760559515,100007106823,100018175376,69760209627,100012417521,100018267032',
        '100018208790,100009828449,100009828451,69920714431,100017163676,100009828465,100017163708,100018208812,100018208824,100018208822,100007309457,100018208828,100013378428,100009828455,100017163674,100018175334,69920714430,100010273219,69774037056,100016161636,100013599790,10029630773255,69882231131,10029713401596,10029630773256,10021077069663,69772354177,10031413109897,69772781261,69625557915']
    zipList = list(zip(pageList, sList, itemsList))
    for perZip in zipList:
        headers = {
            'authority': 'search.jd.com',
            'method': 'GET',
            'path': '/s_new.php?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&qrst=1&suggest=1.his.0.0&wq=%E5%A4%A7%E5%BA%84%E5%9B%AD&stock=1&ev=exbrand_%E5%A4%A7%E5%BA%84%E5%9B%AD%EF%BC%88Grand%20Farm%EF%BC%89%5E&pvid=e9401337a3714baa84c1ca1d58856c3c&cid3=13582&cid2=13581&page=4&s=91&scrolling=y&log_id=1633765366768.2675&tpl=1_M&isList=0&show_items=100018208790,100009828449,100009828451,69920714431,100017163676,100009828465,100017163708,100018208812,100018208824,100018208822,100007309457,100018208828,100013378428,100009828455,100017163674,100018175334,69920714430,100010273219,69774037056,100016161636,100013599790,10029630773255,69882231131,10029713401596,10029630773256,10021077069663,69772354177,10031413109897,69772781261,69625557915',
            'scheme': 'https',
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '__jdu=34820952; shshshfpa=4422ac4e-aae1-bac1-bf5c-7582e3897c2d-1627269659; shshshfpb=dSymlNuOXQ65rxqybfxoFYg%3D%3D; qrsc=3; areaId=0; PCSYCityID=CN_0_0_0; rkv=1.0; ipLoc-djd=1-72-55653-0; user-key=5dccd210-4b6f-4e30-9e8b-d651c7b6b163; unpl=V2_ZzNtbRZeSxBxCkIDexhaDGJXFVgSURESJgxCB3seXlVgABdUclRCFnUURlVnGFQUZgsZWERcQxNFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZHkcVQZmCxZecmdEJUU4QVN5GVkBVwIiXHIVF0lzC0JUfRoRB2IKEVxKU0AldDhF; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e894535f10784e64a7c6b55b163a6248|1633744037873; __jdc=122270672; shshshfp=b38a19b2564624749fd6ebae699a8a78; __jda=122270672.34820952.1626255775.1633756072.1633762929.19; __jdb=122270672.12.34820952|19.1633762929; shshshsID=94744ab6bdb6f87cbb49f0856960a44f_12_1633765367718; 3AB9D23F7A4B3C9B=TA5KAGBNRD4YFUGMDQST52VGH7TGFLYX4UPWD3PBZYB2RBC7IUGG7EUKU3GHBM4ZGFJ73VLDAY3QYIUCY6MY3BGEEU',
            'referer': 'https://search.jd.com/search?keyword=%E5%A4%A7%E5%BA%84%E5%9B%AD&qrst=1&suggest=1.his.0.0&wq=%E5%A4%A7%E5%BA%84%E5%9B%AD&stock=1&ev=exbrand_%E5%A4%A7%E5%BA%84%E5%9B%AD%EF%BC%88Grand%20Farm%EF%BC%89%5E&pvid=e9401337a3714baa84c1ca1d58856c3c&cid3=13582&cid2=13581&page=3&s=61&click=0',
            'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        data = {
            'keyword': '大庄园',
            'qrst': '1',
            'suggest': '1.his.0.0',
            'wq': '大庄园',
            'stock': '1',
            'ev': 'exbrand_大庄园（Grand Farm）^',
            'pvid': 'e9401337a3714baa84c1ca1d58856c3c',
            'cid3': '13582',
            'cid2': '13581',
            'page': str(perZip[0]),
            's': str(perZip[1]),
            'scrolling': 'y',
            'log_id': '1633765035921.6283',
            'tpl': '1_M',
            'isList': '0',
            'show_items': str(perZip[2])
        }
        res = requests.get(url=url, headers=headers, params=data).text
        getData(res)


if __name__ == '__main__':
    item = {}
    getFrontData()
    getBackData()
    cursor.close()
    conn.close()
