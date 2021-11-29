import os
from datetime import datetime

import redis
import pymysql
import pandas as pd

# 链接MySQL数据库
conn = pymysql.Connect(host='10.10.107.7', user='root', password='xinqian@saibao', database='bigdata', port=3306)
cursor = conn.cursor()
# 链接Redis数据库
redisDB = redis.Redis(host='127.0.0.1',port=6379,db=2)
redis_dict_key = 'tianyancha'


def insert_mysql(fileName):
    data = pd.read_excel(fileName, skiprows=[0, 1])
    column_name_list = [column for column in data]
    for eve_data_index in range(len(data[1:])):
        if redisDB.hexists(redis_dict_key,str(data.iloc[eve_data_index][column_name_list[0]])+'-'+str(data.iloc[eve_data_index][column_name_list[2]])+'-'+str(data.iloc[eve_data_index][column_name_list[11]])+'-'+str(data.iloc[eve_data_index][column_name_list[12]])):
            print('该数据已经存在于数据库，不做处理~')
        else:
            insertTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            redisDB.hset(redis_dict_key,str(data.iloc[eve_data_index][column_name_list[0]])+'-'+str(data.iloc[eve_data_index][column_name_list[2]])+'-'+str(data.iloc[eve_data_index][column_name_list[11]])+'-'+str(data.iloc[eve_data_index][column_name_list[12]]),0)
            sql = 'insert into ods_tianyancha(companyName,operationStatus,legalRepresentative,registeredCapital,paidInCapital,dateOfIncorporation,approvalDate,businessTerm,province,city,area,unifiedSocialCreditCode,taxpayerIdentificationNo,registrationNo,organizationCode,numberOfInsuredPersons,companyType,industry,nameUsedBefore,companyRegisteredAddress,latestAnnualReportAddress,website,phone,otherPhone,email,otherEmail,natureOfBusiness,insertTime)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            data.iloc[eve_data_index] = data.iloc[eve_data_index].fillna('')
            cursor.execute(sql, (
                data.iloc[eve_data_index][column_name_list[0]], data.iloc[eve_data_index][column_name_list[1]],
                data.iloc[eve_data_index][column_name_list[2]], data.iloc[eve_data_index][column_name_list[3]],
                data.iloc[eve_data_index][column_name_list[4]], data.iloc[eve_data_index][column_name_list[5]],
                data.iloc[eve_data_index][column_name_list[6]], data.iloc[eve_data_index][column_name_list[7]],
                data.iloc[eve_data_index][column_name_list[8]], data.iloc[eve_data_index][column_name_list[9]],
                data.iloc[eve_data_index][column_name_list[10]], data.iloc[eve_data_index][column_name_list[11]],
                data.iloc[eve_data_index][column_name_list[12]], data.iloc[eve_data_index][column_name_list[13]],
                data.iloc[eve_data_index][column_name_list[14]], data.iloc[eve_data_index][column_name_list[15]],
                data.iloc[eve_data_index][column_name_list[16]], data.iloc[eve_data_index][column_name_list[17]],
                data.iloc[eve_data_index][column_name_list[18]],data.iloc[eve_data_index][column_name_list[19]],
                data.iloc[eve_data_index][column_name_list[20]],data.iloc[eve_data_index][column_name_list[21]],
                data.iloc[eve_data_index][column_name_list[22]],data.iloc[eve_data_index][column_name_list[23]],
                data.iloc[eve_data_index][column_name_list[24]],data.iloc[eve_data_index][column_name_list[25]],
                data.iloc[eve_data_index][column_name_list[26]],insertTime
            ))
            print("新的数据正在插入，请等候...")
            conn.commit()


if __name__ == '__main__':
    file_dir = './天眼查'
    for root, dir, files in os.walk(file_dir):
        for i in files:
            fileName = root + '/' + i
            insert_mysql(fileName)
    cursor.close()
    conn.close()
