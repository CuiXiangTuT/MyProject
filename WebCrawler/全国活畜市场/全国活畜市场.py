import asyncio
import aiohttp
import pymysql
import pandas as pd
import xlwt

# 创建一个新的excel，工作表，并设置前三列的表头
work_book = xlwt.Workbook(encoding='utf-8')
sheet = work_book.add_sheet('全国活畜市场')
sheet.write(0, 0, '该地区市场数量')
sheet.write(0, 1, '市场名称')
sheet.write(0, 2, 'type类型')
sheet.write(0, 3, '地址信息')
sheet.write(0, 4, '位置坐标信息')
sheet.write(0, 5, '电话信息')
sheet.write(0, 6, '省份')
sheet.write(0, 7, '省份代号')
sheet.write(0, 8, '城市')
sheet.write(0, 9, '城市代号')
sheet.write(0, 10, '区域')
sheet.write(0, 11, '区域代号')


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
    row_num = 1
    for eve_data in result:
        # 该地区一共有多少个市场
        item['area_market_count'] = eve_data['count']
        # 获取当前市场信息
        if item['area_market_count'] == '0':
            pass
        else:
            pois_list = eve_data['pois']
            file_market = open('./全国活畜市场.txt', 'a', encoding='utf-8')

            for eve_pois in pois_list:
                # 市场名称
                item['market_name'] = eve_pois['name']
                # type类型
                item['market_type'] = eve_pois['type']
                # 地址信息
                item['market_addr'] = eve_pois['address']
                # 位置坐标信息
                item['market_location'] = eve_pois['location']
                # 电话信息
                item['market_phone'] = eve_pois['tel']
                # 省份
                item['market_location_province'] = eve_pois['pname']
                # 省份代号
                item['market_location_province_code'] = eve_pois['pcode']
                # 城市
                item['market_location_city'] = eve_pois['cityname']
                # 城市代号
                item['market_location_city_code'] = eve_pois['citycode']
                # 区域
                item['market_location_addr'] = eve_pois['adname']
                # 区域代号
                item['market_location_addr_code'] = eve_pois['adcode']
                file_market.write(str(item))
                file_market.write('\n')
                sheet.write(row_num, 0, item['area_market_count'])
                sheet.write(row_num, 1, item['market_name'])
                sheet.write(row_num, 2, item['market_type'])
                sheet.write(row_num, 3, item['market_addr'])
                sheet.write(row_num, 4, item['market_location'])
                sheet.write(row_num, 5, item['market_phone'])
                sheet.write(row_num, 6, item['market_location_province'])
                sheet.write(row_num, 7, item['market_location_province_code'])
                sheet.write(row_num, 8, item['market_location_city'])
                sheet.write(row_num, 9, item['market_location_city_code'])
                sheet.write(row_num, 10, item['market_location_addr'])
                sheet.write(row_num, 11, item['market_location_addr_code'])
                row_num += 1

            file_name = './全国活畜市场.xlsx'
            work_book.save(file_name)
            file_market.close()


def run(province_list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
    }

    for province in province_list:
        url = 'https://restapi.amap.com/v3/place/text?key=23fa8695df583dd27453d150d2289831&keywords=%E6%B4%BB%E7%95%9C&types=&city={}&children=1&offset=500&page=1&extensions=all'
        task = asyncio.ensure_future(getData(url.format(province), headers))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    saveData(result)


if __name__ == '__main__':
    province_list = get_province()
    tasks = []
    loop = asyncio.get_event_loop()
    run(province_list)
