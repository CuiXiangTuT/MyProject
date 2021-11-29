# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
import redis
from itemadapter import ItemAdapter


class DongpinyigangshanghudatingPipeline:
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
        self.redis_data_dict = 'dpyg_gongying'
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
                                 item['title'] + '-' + str(item['u_id']) + '-' + str(item['companyId']) + '-' + item['update_time']):
            # 若存在，输出数据库已经存在该数据
            print('数据库中已经存在该数据,不做处理~~~')
            # print('数据库中已经存在该数据,做更新处理')
            # sql = "UPDATE ods_dpyg_gongying SET username=%s,business=%s WHERE product_name = %s AND contact_person_phone = %s"
            # self.cursor.execute(sql, (
            # item['username'], item['business'], item['product_name'], item['contact_person_phone']))
            # self.db.commit()

        else:
            # 若不存在，则将URL写入Redis数据库中
            # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
            self.redis_db.hset(self.redis_data_dict,
                               item['title'] + '-' + str(item['u_id']) + '-' + str(item['companyId']) + '-' + item['update_time'], 0)
            # 进行MySQL入库处理
            sql = "insert into ods_dpyg_gongying(title,goodsCategory,goodsAmount,unitName,packageUnit,productCode,goodsPrice,origin,isTop,provinceName,provinceId,unitId,factoryNo,u_id,cityName,cityId,memberGradeId,companyName,companyId,address,userId,business_name,contactsPhone,StartingBatch,specificationValue,isOpenPayment,licenseImage,isBill,update_time,cur_time,goodsType,goodsTypeDetail) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (
                item['title'], item['goodsCategory'], item['goodsAmount'], item['unitName'], item['packageUnit'],
                item['productCode'],
                item['goodsPrice'], item['origin'], item['isTop'], item['provinceName'], item['provinceId'],
                item['unitId'], item['factoryNo'], item['u_id'], item['cityName'], item['cityId'],
                item['memberGradeId'], item['companyName'], item['companyId'], item['address'], item['userId'],
                item['business_name'], item['contactsPhone'], item['StartingBatch'],
                item['specificationValue'], item['isOpenPayment'], item['licenseImage'], item['isBill'],
                item['update_time'], item['cur_time'],item['goodsType'],item['goodsTypeDetail']))
            self.db.commit()
        return item
