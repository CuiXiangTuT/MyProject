import asyncio
import aiohttp
import pymysql
import pandas as pd
import xlwt




# 获取各省份
def get_province():
    conn = pymysql.Connection(user='root', password='xinqian@saibao', host='10.10.107.7', database='bigdata', port=3306)
    province_data = pd.read_sql('select * from d_bs_province;', conn)
    return list(province_data['SHORT_NAME'])


async def getData(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


def saveData(result):

    item = {}

    file_market = open('./全国餐饮市场/全国餐饮市场.txt', 'a+', encoding='utf-8')
    for eve_data in result:
        if eve_data['info'] == 'OK':
            # 该地区一共有多少个市场
            item['area_market_count'] = eve_data['count']
            # 获取当前市场信息
            if item['area_market_count'] == '0':
                pass
            else:
                row_num = 1
                # 创建一个新的excel，工作表，并设置前三列的表头
                work_book = xlwt.Workbook(encoding='utf-8')
                sheet = work_book.add_sheet('全国餐饮市场')
                sheet.write(0, 0, 'id')
                sheet.write(0, 1, 'name')
                sheet.write(0, 2, 'tag')
                sheet.write(0, 3, 'type')
                sheet.write(0, 4, 'typecode')
                sheet.write(0, 5, 'biz_ext')
                sheet.write(0, 6, 'address')
                sheet.write(0, 7, 'location')
                sheet.write(0, 8, 'tel')
                sheet.write(0, 9, 'pname')
                sheet.write(0, 10, 'cityname')
                sheet.write(0, 11, 'adname')
                sheet.write(0, 12, 'photos')
                pois_list = eve_data['pois']
                for eve_pois in pois_list:
                    # id
                    item['id'] = eve_pois['id']
                    # name
                    item['name'] = eve_pois['name']
                    # tag
                    item['tag'] = eve_pois['tag']
                    # type
                    item['type'] = eve_pois['type']
                    # typecode
                    item['typecode'] = eve_pois['typecode']
                    # biz_type
                    item['biz_type'] = eve_pois['biz_type']
                    # address
                    item['address'] = eve_pois['address']
                    # location
                    item['location'] = eve_pois['location']
                    # tel
                    tel = eve_pois['tel']
                    if tel:
                        item['tel'] = tel
                    else:
                        item['tel'] = '无'

                    # p_name
                    item['pname'] = eve_pois['pname']
                    # cityname
                    item['cityname'] = eve_pois['cityname']
                    # adname
                    item['adname'] = eve_pois['adname']
                    # photos
                    photos_list = eve_pois['photos']
                    if len(photos_list):
                        for per_photo in eve_pois['photos']:
                            item['photos'] = per_photo['url']
                            file_market.write(str(item))
                            file_market.write('\n')
                            sheet.write(row_num, 0, item['id'])
                            sheet.write(row_num, 1, item['name'])
                            sheet.write(row_num, 2, item['tag'])
                            sheet.write(row_num, 3, item['type'])
                            sheet.write(row_num, 4, item['typecode'])
                            sheet.write(row_num, 5, item['biz_type'])
                            sheet.write(row_num, 6, item['address'])
                            sheet.write(row_num, 7, item['location'])
                            sheet.write(row_num, 8, item['tel'])
                            sheet.write(row_num, 9, item['pname'])
                            sheet.write(row_num, 10, item['cityname'])
                            sheet.write(row_num, 11, item['adname'])
                            sheet.write(row_num, 12, item['photos'])
                            row_num += 1
                            file_name = './全国餐饮市场/全国餐饮市场' + '-' + str(eve_data['pois'][0]['pname']) + '-' + str(
                                result.index(eve_data)) + '.xlsx'
                            work_book.save(file_name)


                    else:
                        item['photos'] = ''
                        file_market.write(str(item))
                        file_market.write('\n')
                        sheet.write(row_num, 0, item['id'])
                        sheet.write(row_num, 1, item['name'])
                        sheet.write(row_num, 2, item['tag'])
                        sheet.write(row_num, 3, item['type'])
                        sheet.write(row_num, 4, item['typecode'])
                        sheet.write(row_num, 5, item['biz_type'])
                        sheet.write(row_num, 6, item['address'])
                        sheet.write(row_num, 7, item['location'])
                        sheet.write(row_num, 8, item['tel'])
                        sheet.write(row_num, 9, item['pname'])
                        sheet.write(row_num, 10, item['cityname'])
                        sheet.write(row_num, 11, item['adname'])
                        sheet.write(row_num, 12, item['photos'])
                        row_num += 1

                        file_name = './全国餐饮市场/全国餐饮市场'+'-'+str(eve_data['pois'][0]['pname'])+'-'+str(result.index(eve_data))+'.xlsx'
                        work_book.save(file_name)
    file_market.close()



def run(province_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
    }

    for province in province_list:
        for j in range(1,20):
            url = 'https://restapi.amap.com/v3/place/text?key=23fa8695df583dd27453d150d2289831&keywords=%E7%89%9B%E7%BE%8A&types=&city={}&children=1&offset=50&page={}&extensions=all'
            task = asyncio.ensure_future(getData(url.format(province,str(j)), headers))
            tasks.append(task)
    # print(tasks)
        result = loop.run_until_complete(asyncio.gather(*tasks))
        saveData(result)


if __name__ == '__main__':
    province_list = get_province()
    tasks = []
    loop = asyncio.get_event_loop()
    run(province_list)
