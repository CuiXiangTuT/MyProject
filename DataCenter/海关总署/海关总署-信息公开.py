import requests


def get_list_data():
    url = "http://search.customs.gov.cn/search/pcRender?pageId=f5261418ddc74f03b27e3590c531102b"
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        # 'Connection': 'keep-alive',
        'Content-Length': '621',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'AMJ-VISIT=A62F6F5AE9A44D708763AA6BE232CE1B,34cnL1KET_8pwCG9bHCnEiXEBGPL4QvZG39UL7A6rjxHrBnIdLSh!-1242597615!1637039952516,1636977647000; _gscu_1524496263=28652768s22zbs12; 9CKCOkIaqzqES=5OmJHPhUaC9tM5DjZmzZBMaiXbUvjV17FI3bIHzFDWY7w8w70NFAbMHoss_vzyYO_66NI_2BgWeBQhablOSPRFq; _gscbrs_1524496263=1; searchLogs=[{"title":"ç”µå­ç¨Žå•","pagename":"æˆ‘è¦æŸ¥","url":"http://43.248.49.212/tax2017"}]; _gsref_1524496263=http://search.customs.gov.cn/; JSESSIONID=34cnL1KET_8pwCG9bHCnEiXEBGPL4QvZG39UL7A6rjxHrBnIdLSh!-1242597615; visitorLogs=[{"title":"ä¸­æ¾³è‡ªè´¸åå®šå®žæ–½ä¸€å‘¨å¹´ å±±ä¸œ300å¤šå®¶ä¼ä¸šå—ç›Š","pagename":"ä»Šæ—¥æµ·å…³","url":"http://www.customs.gov.cn/customs/xwfb34/302425/636122/index.html"},{"title":"å…³äºŽç¦æ­¢è‹±å›½30æœˆé¾„ä»¥ä¸‹å‰”éª¨ç‰›è‚‰è¿›å£çš„å…¬å‘Šè§£è¯»","pagename":"æ”¿ç­–è§£è¯»","url":"http://www.customs.gov.cn//customs/302249/302270/302272/3984631/index.html"},{"title":"ï¼ˆæµ·å…³æ€»ç½²ï¼‰ 2021å¹´4ï¼ˆè‡³ï¼‰5æœˆæ”¿åºœé‡‡è´­æ„å‘","pagename":"æ”¿åºœé‡‡è´­","url":"http://nanjing.customs.gov.cn/customs/302249/zfxxgk/2799825/302306/3566087/index.html"}]; _gscs_1524496263=t37039888kf40xk20|pv:3; 9CKCOkIaqzqET=5FxLCIbPFJvqxcAf0hO9HMA917Dnu8pnYE4py94WwN9835f1aMdaQWE4.fwWYSomA.wmHkp.UnpDZYVc6x_hMLKwrIE3P3FchwssGoHYHkCuLEyU6uc6k70wZMkiM__pGeYLsMPaCXbbG4yRg8unE9_rF4wSr4kw.9tBlJYvAkjTfWv9a0h_Sjlds2KMLPcVou1RamFFqf3lVA2aPYa7L_zMZ_vzNJO09I8gq_USYCyBEywqrARgQbKZfEzk4dIN4JaMTyxxLOqTEBBTuJWghqYYYMQFJUeHag75Wfz7f6kLtwKaWLIWf9CUW2yLYfDOjE'.encode("utf-8").decode("latin1"),
        'Host': 'search.customs.gov.cn',
        'Origin': 'http://search.customs.gov.cn',
        'Referer': 'http://search.customs.gov.cn/search/pcRender?pageId=f5261418ddc74f03b27e3590c531102b',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
    }
    data = {
        'originalSearchUrl': '/search/pcRender?pageId=f5261418ddc74f03b27e3590c531102b',
        'originalSearch': '',
        'app': '03735b2027db47d8a778436a3908487f,e65985bb34a54d51976b7e944f13b36a,089f6418cf964d30bbdf7ae381ff62a6,2669a851a9ae4bc587ee30efd697d576,918463d4c4d74aa0a543eaf5b84f6e83,8be31e0d6f9d4cd4b34a3d47e43be28a,63577581d629499db69cfda593c49816,a1cd85fd3b2549738ddfcda2b715c6d8,5239bbdf13f0459ea0bf6709d537be2c,6ba1ae8b61e640378a3e2052665badae',
        'appName': '信息公开',
        'sr': 'score desc',
        'advtime': '',
        'advrange': '',
        'ext': 'siteId:300632',
        'pNo': '',
        'advepq': '',
        'advoq': '',
        'adveq': '',
        'searchArea': '',
        'advSiteArea': '',
        'q': '牛肉',
    }
    response = requests.post(url=url, headers=headers, data=data).text
    print(response)


get_list_data()
