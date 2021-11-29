# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
import redis
from itemadapter import ItemAdapter


class AicaigouhuoyuanPipeline:
    def __init__(self, host, user, password, port, database, redis_host, redis_port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.redis_host = redis_host
        self.redis_port = redis_port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            redis_host=crawler.settings.get('REDIS_HOST'),
            redis_port=crawler.settings.get('REDIS_PORT')
        )

    def open_spider(self, spider):
        # 链接Redis数据库,db数据库默认连接到1
        self.redis_db = redis.Redis(host=self.redis_host, port=self.redis_port, db=2)
        # keys名字，里面的内容可以随便给，这里的keys相当于字典名称，而不是key值
        self.redis_data_dict = 'acg_huoyuan'
        # 链接MySQL数据库
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database,
                                  port=self.port, charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        # self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        # 判断Redis数据库中是否存在URL
        # hexists检查给定域中是否存与于哈希表中，若存在，则返回1，不存在则返回0
        if self.redis_db.hexists(self.redis_data_dict,
                                 str(item['id_acg']) + '-' + str(item['query']) + '-' + str(
                                     item['wechatNumber']) + '-' +
                                 str(item['contact']) + '-' + str(item['fullname'])):
            # 若存在，输出数据库已经存在该数据
            print('数据库中已经存在该数据,不做处理~~~')
            # print('数据库中已经存在该数据,做更新处理')
            # sql = "UPDATE ods_dpyg_caigou SET companyName=%s,address=%s WHERE companyId = %s AND title = %s"
            # self.cursor.execute(sql, (
            #     item['companyName'], item['address'], item['companyId'], item['title']))
            # self.db.commit()

        else:
            # 若不存在，则将URL写入Redis数据库中
            # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
            self.redis_db.hset(self.redis_data_dict,
                               str(item['id_acg']) + '-' + str(item['query']) + '-' + str(item['wechatNumber']) + '-' +
                               str(item['contact']) + '-' + str(item['fullname']), 0)
            # 进行MySQL入库处理
            sql = "insert into ods_acg_huoyuangongying(id_acg,category,qid,from_source,location,query,fullname,category_,price,priceCurrency,unitCode,min_Value,max_Value,contact,phone,email,contactName,wechatNumber,externalAddress,address_v2,address,addr,province,city,district,street,userDetail,provider_name,provider_status,provider_regCap,provider_regAddr,provider_scope,provider_jumpUrl,cur_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (
                item['id_acg'], item['category'], item['qid'], item['from_source'],
                item['location'],
                item['query'], item['fullname'], item['category_'], item['price'],
                item['priceCurrency'],
                item['unitCode'], item['minValue'], item['maxValue'], item['contact'], item['phone'],
                item['email'], item['contactName'],
                item['wechatNumber'], item['externalAddress'], item['address_v2'], item['address'], item['addr'],
                item['province'], item['city'], item['district'], item['street'], item['userDetail'],
                item['provider_name'], item['provider_status'], item['provider_regCap'], item['provider_regAddr'],
                item['provider_scope'], item['provider_jumpUrl'], item['cur_time']))
            self.db.commit()
        return item
