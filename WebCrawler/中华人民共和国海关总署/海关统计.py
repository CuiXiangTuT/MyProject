import requests


url = 'http://search.customs.gov.cn/search/pcRender?pageId=f5261418ddc74f03b27e3590c531102b'
headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'AMJ-VISIT=E2C8C86660E343DBAD5F972661E57DBF,a3UMd_BsI3L78RbLPVqCGkkUvGiRdDsmeGvH9JTBHm4w6KU1riUi!-1242597615!1632296759404,1632281937000; _gscu_1524496263=28652768s22zbs12; 9CKCOkIaqzqES=5OmJHPhUaC9tM5DjZmzZBMaiXbUvjV17FI3bIHzFDWY7w8w70NFAbMHoss_vzyYO_66NI_2BgWeBQhablOSPRFq; visitorLogs=[{"title":"æµ·å…³æ€»ç½² å†œä¸šå†œæ‘éƒ¨å…¬å‘Š2020å¹´ç¬¬34å·ï¼ˆå…³äºŽè§£é™¤è¿›å£ç¾Žå›½ç‰›è‚‰åŠç‰›è‚‰äº§å“æœˆé¾„é™åˆ¶çš„å…¬å‘Šï¼‰","pagename":"æµ·å…³æ³•è§„","url":"http://www.customs.gov.cn/customs/302249/302266/302267/2879966/index.html"},{"title":"ã€åŠ¨æ¤ç‰©æ£€ç–«ã€‘ä»€ä¹ˆæ˜¯é«˜è‡´ç—…æ€§ç¦½æµæ„Ÿ?","pagename":"æ”¿ç­–è§£è¯»","url":"http://www.customs.gov.cn/customs/302249/302270/302272/3838321/index.html"},{"title":"å…¬å‘Šè§£è¯»ï¼šå…³äºŽè¿›å£ä¹Œå…¹åˆ«å…‹æ–¯å¦æŽå­å¹²æ£€éªŒæ£€ç–«è¦æ±‚çš„å…¬å‘Š","pagename":"æ”¿ç­–è§£è¯»","url":"http://www.customs.gov.cn/customs/302249/302270/302272/3842627/index.html"}]; JSESSIONID=a3UMd_BsI3L78RbLPVqCGkkUvGiRdDsmeGvH9JTBHm4w6KU1riUi!-1242597615; 9CKCOkIaqzqET=5FlHK4KfkTXaxcAfTrUiwxA3MKptShD2jF68oio.Yo9lszKJKMObSUN9AapLzGcJ2BBtJkgPcKfIQuf0MriHlhEpWEMT1RxURRju6.6FRuyiCXSLGhoyAbZzcnEUXW2IQvtwAh4CzGXyUwlNeXJcxiiKPvRzSOa60zwkp2_GZt4PQymLqpBv30rWI3V_jdWDmxMIC1BSeQ7Q.IfVI.4mAz0iJG_41.KQvnO51co17J_t5Knj.KFyZFDqUaw96TCPHcOvuJYH5EQlhJdEhCA49Ts'.encode('utf-8').decode('latin'),
'Host':'search.customs.gov.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36',
}
data = {
'originalSearchUrl':'/search/pcRender?pageId=f5261418ddc74f03b27e3590c531102b',
'originalSearch':'',
'app':'03735b2027db47d8a778436a3908487f,e65985bb34a54d51976b7e944f13b36a,089f6418cf964d30bbdf7ae381ff62a6,2669a851a9ae4bc587ee30efd697d576,918463d4c4d74aa0a543eaf5b84f6e83,8be31e0d6f9d4cd4b34a3d47e43be28a,63577581d629499db69cfda593c49816,a1cd85fd3b2549738ddfcda2b715c6d8,5239bbdf13f0459ea0bf6709d537be2c,6ba1ae8b61e640378a3e2052665badae',
'appName':'海关统计',
'sr':'score desc',
'advtime':'',
'advrange':'',
'ext':'siteId:300632',
'pNo':'',
'advepq':'',
'advoq':'',
'adveq':'',
'searchArea':'',
'advSiteArea':'',
'q':'牛肉',
}
res = requests.post(url=url,headers=headers,data=data)
print(res.content.decode('utf-8'))