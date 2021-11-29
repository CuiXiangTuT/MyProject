# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#
#
# # useful for handling different item types with a single interface
# import pymysql
# import redis
# from itemadapter import ItemAdapter
#
#
# class BeefuPipeline:
#     def __init__(self, host, user, password, port, database, redis_host, redis_port):
#         self.host = host
#         self.user = user
#         self.password = password
#         self.port = port
#         self.database = database
#         self.redis_host = redis_host
#         self.redis_port = redis_port
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             host=crawler.settings.get('MYSQL_HOST'),
#             user=crawler.settings.get('MYSQL_USER'),
#             password=crawler.settings.get('MYSQL_PASSWORD'),
#             port=crawler.settings.get('MYSQL_PORT'),
#             database=crawler.settings.get('MYSQL_DATABASE'),
#             redis_host=crawler.settings.get('REDIS_HOST'),
#             redis_port=crawler.settings.get('REDIS_PORT')
#         )
#
#     def open_spider(self, spider):
#         # 链接Redis数据库,db数据库默认连接到1
#         self.redis_db = redis.Redis(host=self.redis_host, port=self.redis_port, db=1)
#         # keys名字，里面的内容可以随便给，这里的keys相当于字典名称，而不是key值
#         self.redis_data_dict = 'keyrbf'
#         # 链接MySQL数据库
#         self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database,
#                                   port=self.port, charset='utf8')
#         self.cursor = self.db.cursor()
#
#     def close_spider(self, spider):
#         # self.cursor.close()
#         self.db.close()
#
#     def process_item(self, item, spider):
#         # 判断Redis数据库中是否存在URL
#         # hexists检查给定域中是否存与于哈希表中，若存在，则返回1，不存在则返回0
#         if self.redis_db.hexists(self.redis_data_dict, item['content']):
#             # 若存在，输出数据库已经存在该数据
#             print('数据库中已经存在该数据，为其做更新...')
#             sql = 'update bifu set contact_person_name=%s, company=%s,phone=%s,cur_time=%s where content = %s'
#             self.cursor.execute(sql, (
#             item['contact_person_name'], item['company'], item['phone'], item['cur_time'],
#             item['content']))
#             self.db.commit()
#         else:
#             # 若不存在，则将URL写入Redis数据库中
#             # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
#             self.redis_db.hset(self.redis_data_dict, item['content'], 0)
#             # 进行MySQL入库处理
#             sql = "insert into bifu(contact_person_name,company,phone,content,cur_time) values (%s,%s,%s,%s,%s)"
#             self.cursor.execute(sql, (item['contact_person_name'], item['company'], item['phone'], item['content'], item['cur_time']))
#             self.db.commit()
#         # # 进行MySQL入库处理
#         # sql = "insert into bifusum(productName,meat_name,placeOrigin,factoryNm,realName,phone,releaseTime,buy_supply,data_source,cur_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#         # self.cursor.execute(sql, (
#         #     item['productName'], item['meat_name'], item['placeOrigin'], item['factoryNm'], item['realName'],
#         #     item['phone'], item['releaseTime'], item['buy_supply'], item['data_source'], item['cur_time']))
#         # self.db.commit()
#         return item
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
import redis
from itemadapter import ItemAdapter


class BeefuPipeline:
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
        self.redis_data_dict = 'bifu'
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
        if self.redis_db.hexists(self.redis_data_dict, str(item['new_content'])):
            # 若存在，输出数据库已经存在该数据
            print('数据库中已经存在该数据，不作操作...')
            # sql = 'update bifu_lastest set company=%s,contact_person_name=%s, buy_supply=%s,location=%s,phone=%s,pid=%s,product=%s,content=%s,cur_time=%s where content = %s'
            # self.cursor.execute(sql, (
            #  item['company'],item['contact_person_name'], item['buy_supply'], item['location'],item['phone'],
            # item['pid'],item['product'],item['content'],item['cur_time']))
            # self.db.commit()
        else:
            # 若不存在，则将URL写入Redis数据库中
            # 把key字段的值都设为0，要设成什么都可以，因为后面对比的是字段，而不是值
            self.redis_db.hset(self.redis_data_dict, str(item['new_content']), 0)
            # 进行MySQL入库处理
            sql = "insert into bifu_lastest(company,contact_person_name,buy_supply,location,phone,pid,product,content,cur_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(sql, (
                item['company'], item['contact_person_name'], item['buy_supply'], item['location'], item['phone'],
                item['pid'], item['product'], item['content'], item['cur_time']))
            self.db.commit()
        # # 进行MySQL入库处理
        # sql = "insert into bifusum(productName,meat_name,placeOrigin,factoryNm,realName,phone,releaseTime,buy_supply,data_source,cur_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # self.cursor.execute(sql, (
        #     item['productName'], item['meat_name'], item['placeOrigin'], item['factoryNm'], item['realName'],
        #     item['phone'], item['releaseTime'], item['buy_supply'], item['data_source'], item['cur_time']))
        # self.db.commit()
        return item
