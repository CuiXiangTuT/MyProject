import random
from oss_transform_img import transform_url
from datetime import datetime
import pymysql
import redis
from lxml import etree
import requests
from get_proxies import get_ip_list


# 链接MySQL数据库
conn = pymysql.Connect(user="dc", password="tB*_SGCri8Mcv2&", host="ods.meatdc.com", database="meatdc-ods", port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1', port=6379, db=3)
redis_dict_key = 'ods_bifu_hangqingNews'


def insert_mysql(item):
    if redisDB.hexists(redis_dict_key, str(item['title']) + '-' + str(item['publish_time'])):
        print('已存在该数据，不作处理~~~')
    else:
        redisDB.hset(redis_dict_key, str(item['title']) + '-' + str(item['publish_time']), 0)
        sql = "insert into ods_weixin_gongzhonghao(title,publishTime,isOriginalArticle,author,content,gzhSource,originalURL,insertTime) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, (
            item['title'], item['publish_time'], item['is_original_article'], item['author'], item['content'],
            item['gzh_source'], item['original_url'], item['insert_time']))
        conn.commit()
        print('数据正在插入，请稍后...')


def get_detail_data(url):
    """
    获取详情页数据
    :param url: 详情页url
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36'
    }
    res_text = requests.get(url=url, headers=headers).text
    response = etree.HTML(res_text)
    # 是否含有原创
    try:
        item['is_original_article'] = response.xpath('.//span[@id="copyright_logo"]//text()')[0]
    except:
        item['is_original_article'] = ''
    # 作者
    try:
        item['author'] = response.xpath(
            './/span[contains(@class,"rich_media_meta") and contains(@class,"rich_media_meta_text")]/text()')[0].strip()
    except:
        item['author'] = ''
    # 内容
    sectionList = response.xpath('//div[@id="js_content"]//text()|//div[@id="js_content"]//img/@data-src')

    content_list = []

    for i in sectionList:

        if 'http' in i:
            new_url = transform_url(i)
            img_url = '<img src="' + new_url + '">'
            content_list.append(img_url)
        elif i.strip():
            content_list.append(i)
        else:
            pass
    content = '<br/>'.join(content_list)
    # # 获取词频
    # item["word_frequency"] = get_word_frequency(item["title"], content, total_list)
    # # 给该文章打分
    # item["score"] = manage_time_score(item["publish_time"])
    item['content'] = content
    item['insert_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_mysql(item)
    print(item)


def get_list_data(wechat_list):
    """
    将详情页url添加进去一个获取数据
    :param wechat_list: 公众号列表
    :return:
    """
    for wechat in wechat_list:
        url = 'https://newrank.cn/xdnphb/detail/v1/rank/article/lists'

        headers = {
            'cookie': 'tt_token=true; Hm_lvt_a19fd7224d30e3c8a6558dcb38c4beed=1634197575; UM_distinctid=17c7dc4157e929-0c13d9b68e40c3-6d56732a-1fa400-17c7dc4157f4e7; CNZZDATA1253878005=47512762-1634190697-https%253A%252F%252Fwww.newrank.cn%252F%7C1634190697; token=553389DE63B945278FFCA5C974E21BE2; Hm_lpvt_a19fd7224d30e3c8a6558dcb38c4beed=1634197599; tt_token=true',
            'origin': 'https://newrank.cn',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
        }
        data = wechat[1]
        ip = random.choice(ip_list)
        try:
            json_total_list = requests.post(url=url, headers=headers, data=data,
                                            proxies={'http': 'http://' + ip['ip'] + ':' + ip['port']}).json()['value'][
                'articles']
            item['gzh_source'] = wechat[0]
            for perJson in json_total_list[0]:
                # 标题
                item['title'] = perJson['title']
                # 时间
                item['publish_time'] = perJson['publicTime']
                # url
                detail_url = perJson['url']
                item['original_url'] = detail_url
                get_detail_data(detail_url)
        except:
            pass


def get_wechat():
    """
    将微信公众号列表与参数data进行打包
    :return: 列表，列表里面是以字典形式保存的数据，{"公众号1":"参数data1"}
    """
    wechat_list = ["牛羊宝典", "现代畜牧每日电讯", "牛羊班", "冻品行情", "今日牛羊", "牛人一得", "肉类360", "国际畜牧网", "新牧网", "肉类工业杂志", "肉交所",
                   "BEEF常熟市丝绸之路", "商品交易场所创新服务智库", "优合集团优顶特研究院", "艾瑞咨询", "中物联冷链委", "运联智库", "物流时代周刊", "中国航务周刊",
                   "运去哪", "航运交易公报", "海关发布", "福来神农岛"]

    data_list = [{
        'account': 'nybd2019',
        'nonce': '06c7921ea',
        'xyz': 'cc81539bcb5fd0ee05b1d5ccbdb5c1d7'},
        {
            'account': 'cvonet2010',
            'nonce': '72e98f1a3',
            'xyz': 'eaba561c92d0ab9d659f09afd69f906f'
        }, {
            'account': 'niuyangban888',
            'nonce': 'd5283f14c',
            'xyz': '7ba652cb591cb02e3d12ae8319176189'
        }, {
            'account': 'dongpinhangqing',
            'nonce': '17cd56480',
            'xyz': '09b598ff458118b95d2afe1935f4c13d'
        }, {
            'account': 'jinriniuyang',
            'nonce': '60d72953e',
            'xyz': '4530f2d327797b1763439644ab87ea86'
        }, {
            'account': 'beefman888',
            'nonce': 'd5ef41c3a',
            'xyz': '94f6f24cdef56ae10229c3e877e9de92'
        }, {
            'account': 'www_meat360_cn',
            'nonce': '6b59c2713',
            'xyz': '211741a4fbdeae1857d3c0c024f3be6a'
        }, {
            'account': 'guojixumuwang',
            'nonce': '06d4ea92b',
            'xyz': '05a0987b1e7a5842b6649478c65dc0dc'
        }, {
            'account': 'xinmunet',
            'nonce': 'd36ec729a',
            'xyz': 'ac1b52d1b70de6cbd432d14626740a6b'
        }, {
            'account': 'meat-industry',
            'nonce': 'de57b9084',
            'xyz': '800893ff034099f99d1b8b7c1d8627af'
        }, {
            'account': 'roujiaosuo',
            'nonce': '32fea9cd0',
            'xyz': 'f3b30155e1a7b6a0a5e2ab742ed30f5d'
        }, {
            'account': 'CSSCZL777',
            'nonce': '80cbd1495',
            'xyz': '6c9a2fbb1cd47fc2869eafe94883d13f'
        }, {
            'account': 'gh_9219fac6fa87',
            'nonce': 'e310584dc',
            'xyz': 'bbc1f530ea2c7dbeda78c17d3d877f9d'
        }, {
            'account': 'OIGResearch',
            'nonce': '7af0b3d18',
            'xyz': 'bba2ac71badb66148f94d1302d50c3c6'
        }, {
            'account': 'iresearch-',
            'nonce': 'bef160572',
            'xyz': 'bac7b69859fd0de2c975aef6a3c1dd34'
        }, {
            'account': 'lenglian_56',
            'nonce': 'f1ea4d590',
            'xyz': 'c02b801be2e04c2422470eddcefd5adf'
        }, {
            'account': 'tucmedia',
            'nonce': '41cba60de',
            'xyz': 'ba28a2eeca01fa0063ebf6ea4da184f6'
        }, {
            'account': 'wuliushidai',
            'nonce': '392bf8d4c',
            'xyz': '63dcaf183dde8a54759edca0e761bef4'
        }, {
            'account': 'chinashippinggazette',
            'nonce': 'ce270b1f9',
            'xyz': 'cda25ac90ae33f89df5721525fbb5117'
        }, {
            'account': 'yunquna_news',
            'nonce': 'd90fc51b6',
            'xyz': '36d2c912c946e9ca6a43cbb26bb07417'
        }, {
            'account': 'sebweekly',
            'nonce': 'bd39208ca',
            'xyz': '1525793a705cdc343cfdb9d91df43fa4'
        }, {
            'account': 'haiguanfabu',
            'nonce': 'd7986eba5',
            'xyz': 'e0f0af5e0b41f16a9790dde0fb51aefd'
        }, {
            'account': 'sndfly',
            'nonce': '312a0bec9',
            'xyz': '99e142b404f99d4465074e58d713768b'
        }]

    zip_list = list(zip(wechat_list, data_list))
    return zip_list


if __name__ == '__main__':
    # total_list = total_class_sort()
    ip_list = get_ip_list()
    wechat_list = get_wechat()
    item = dict()
    get_list_data(wechat_list)
