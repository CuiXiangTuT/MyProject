import oss2
import datetime
import string
import random
import requests


def transform_url(url):
    """
    转换url
    :param url:
    :return:新的图片的url
    """
    # 自定义随机名称
    now = datetime.datetime.now()
    random_name = now.strftime("%Y%m%d%H%M%S") + ''.join([random.choice(string.digits) for _ in range(4)])
    # 自有域名
    cname = 'http://oss.qknyr.com/'
    # 存放OSS路径
    file_name = 'imgFile/{}.jpg'.format(random_name)
    # AccessKeyID和AccessKeySecret
    auth = oss2.Auth('LTAI4GB9G4WAwvxSWS8Sgjae', 'E0oM3ypy2kByHiHmfRqzdS5OhSteaW')
    # 外网访问的Bucket域名和Bucket名称
    bucket = oss2.Bucket(auth, 'http://oss.qknyr.com/', 'qknyr', is_cname=True)
    # 图片链接
    resp = requests.get(url).content
    bucket.put_object(file_name, resp)
    # 最终的图片链接
    new_url = cname + file_name
    return new_url

"""
数据已存在，不作处理...
"""