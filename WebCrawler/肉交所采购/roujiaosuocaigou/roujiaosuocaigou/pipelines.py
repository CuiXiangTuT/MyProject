# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import redis
from itemadapter import ItemAdapter
import pymysql


class RoujiaosuocaigouPipeline:
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
        self.redis_db = redis.Redis(host=self.redis_host, port=self.redis_port, db=1)
        # keys名字，里面的内容可以随便给，这里的keys相当于字典名称，而不是key值
        self.redis_data_dict = 'rjs_caigou'
        # 链接MySQL数据库
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database,
                                  port=self.port, charset='utf8')
        self.cursor = self.db.cursor()

    def close_spider(self, spider):
        # self.cursor.close()
        self.db.close()
        self.redis_db.close()

    def process_item(self, item, spider):
        # 判断Redis数据库中是否存在URL
        # hexists检查给定域中是否存与于哈希表中，若存在，则返回1，不存在则返回0
        if self.redis_db.hexists(self.redis_data_dict,
                                 str(item['product_name']) + str(item['iphone']) + str(item['intention_price']) + str(
                                     item['intention_count'])):
            # 若存在，输出数据库已经存在该数据，并对其做更新处理
            print('数据库中已经存在该数据，做更新处理...')

            sql = "update rjs_caigou set username=%s where product_name = %s and iphone = %s"
            self.cursor.execute(sql, (
                item['username'], item['product_name'],
                item['iphone']))
            self.db.commit()
        else:
            # 若不存在，则将URL写入Redis数据库中
            # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
            self.redis_db.hset(self.redis_data_dict,
                               str(item['product_name']) + str(item['iphone']) + str(item['intention_price']) + str(
                                   item['intention_count']), 0)
            # 进行MySQL入库处理
            sql = "insert into rjs_caigou(product_name,meat_name,sec_catname,truename,iphone,intention_price,intention_count,buy_requirements,edittime,province,city,origin_requirements,status_requirements,pubbuy,telcount,buy_supply,data_source,cur_time,username) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (
                item['product_name'], item['meat_name'], item['sec_catname'], item['truename'], item['iphone'],
                item['intention_price'], item['intention_count'], item['buy_requirements'], item['edittime'],
                item['province'], item['city'],
                item['origin_requirements'], item['status_requirements'], item['pubbuy'],
                item['telcount'], item['buy_supply'], item['data_source'], item['cur_time'], item['username']))
            self.db.commit()
        return item
