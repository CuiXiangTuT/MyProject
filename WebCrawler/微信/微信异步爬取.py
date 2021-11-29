import asyncio
import aiohttp



async def getData(url, headers):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.text()



def saveData(result):
    for i in result:
        soup = BeautifulSoup(i, 'lxml')
        find_div = soup.find_all('div', class_='board-item-content')
        for d in find_div:
            name = d.find('p', class_='name').getText()
            star = d.find('p', class_='star').getText().strip()
            releasetime = d.find('p', class_='releasetime').getText()
            score = d.find('i', class_='integer').getText() + d.find('i', class_='fraction').getText()
            # 写入CSV文件
            csvFile = open('猫眼Top100.csv', 'a', newline='', encoding='utf-8')
            writer = csv.writer(csvFile)
            writer.writerow([name, star, releasetime, score])
            csvFile.close()


def run():
    for i in range(10):
        task = asyncio.ensure_future(getData(url.format(i * 10), headers))
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    saveData(result)


if __name__ == '__main__':
    tasks = []
    loop = asyncio.get_event_loop()
    run()
