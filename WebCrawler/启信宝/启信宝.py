import json

import requests

url = 'https://b.qixin.com/api/search/commonSearch'
headers = {
    # 'authority': 'b.qixin.com',
    # 'method': 'POST',
    # 'path': '/api/search/commonSearch',
    # 'scheme': 'https',
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'authorization': 'undefined',
    # 'b2362ada7fd511be45c5': 'e6b1b89f1e6e0d0d4a7b2b6d3a777817d18c8e774ca16864528b436f3edeae156b89d678f45f23b6f8d4540c5e2b46ee764098037a4dfbb1c959b38b324ebfc8',
    # 'cache-control': 'no-cache',
    # 'content-length': '175',
    'content-type': 'application/json;charset=UTF-8',
    'cookie': 'pdid=s%3AdvIiEsp9KwPPnmWNKVfmCKHklcaM1cR7.McozsOH0sdpmoCLxXGQ0TxhCfTK5SNRMYNRuRyffRzQ; Hm_lvt_52d64b8d3f6d42a2e416d59635df3f71=1629791997,1629792009,1629857723,1629857799; Hm_lpvt_52d64b8d3f6d42a2e416d59635df3f71=1629857958; ssxmod_itna=CqRhDvqjrH0dD=G7CbPiKeAI4Hu+BfDBTbuxiNDnD8x7YDvC7htDG2gR/bu/77WNDuWhGUb/jaRAb43YQbotPtDCPGnDBI0daS4YY7Dt4DTD34DYDixKDLDmeD+zVPDdA1dvt82D3qGrDlKDRx07Z25DWh9D4Oq821cGZaYDnoWCbYx8D75Dux0H8DSwDDHAw8u12hEIjC2DDBRPbeLeieL4bYnDDmRY+P7GDCKDjhBkOa7jLpyCscktiQRPiBDtHCGq4r6eqjq4yA6xOADe8BWP8m2xeGz=aC1l9DDWb7qP8FmDD===; ssxmod_itna2=CqRhDvqjrH0dD=G7CbPiKeAI4Hu+BD8TliqGNGO/DFxbx+Z3oaSW3KAPEdFEhkZ9E25i+MbgT2oD008HXs=s32EWvgKAlWUmMj4CvtCPgzr4cAdu1I37U5rdaxdL3b1+ATGSn3xNFeWKFa6PWWrvWMiyt5WKkz1xrF7KwbBA+HQFQ3I+HH873e/FHsb834+mhb/mG3I8bOFyFZBnxBErWooS=EiyQp22j5C4e48cPvQD1XOljbErQ9pvi2RyvFs+IWhgblipClZnmDonmzVevpVW+Dha95EURNcZoQFVrU4WfP3cyO6PnjwxrP4Iqt6KhYXUQtqSvcAqQPI=ZYx9tUY0uh2vm=jep0YighP=+pe6myO0jOURW6DRrq/2EY5YG4vme4QpAmQveTkUPLBq+2usSqFm+mo5++INYTsjTO04TCqA3h8FW==agCR+3xkGI76c0=cEpWP0mE7PYCFv7pLQQDZQI7q9Sqg+9A/WL0mc/QPY4DQ9N78HLdfQfKeeKirV7b=mxqlhKm3hL+wXDmVqzSypbRPKGFKinUhCBjQ/jNmDtyl6Q6s74eK=fO6v16y8Mz=3eSrAZfC7+K9pu70OdnDUG=rq=akj=tRO2Db=DFqD+=yfzD4AO4GW7um6N8znLIm+qBa4B6UHPaHGkmzoye7yaIG/I7GqiludD===; Hm_lvt_26ffd1a451646e73421b247bc5f91636=1629857990; href=https%3A%2F%2Fb.qixin.com%2F%3Ffrom%3Dindex; accessId=b1ef3bb0-32e4-11eb-8a9d-c52ba771e9fa; pageViewNum=1; bad_idb1ef3bb0-32e4-11eb-8a9d-c52ba771e9fa=ec701552-054a-11ec-875d-fdb64ab942ec; nice_idb1ef3bb0-32e4-11eb-8a9d-c52ba771e9fa=ec701553-054a-11ec-875d-fdb64ab942ec; acw_tc=2f624a4816298624574945755e7be205a5ad39dbd8c801916ea5ffd055058a; sid=s%3APEbWD17Ci3uDi8BBeVKZ3n5FXPV8LpfW.BhdB9Jw0stRp2xXDy4Bh9ECBteCsEqxKkAKeQavvg5k; Hm_lpvt_26ffd1a451646e73421b247bc5f91636=1629862709',
    # 'origin': 'https://b.qixin.com',
    # 'pragma': 'no-cache',
    # 'referer': 'https://b.qixin.com/search/advanced',
    # 'request-id': '48ee2aa1-ac14-41e2-8430-c35edeea4f1e',
    # 'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.8 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = {"ScoreField": [], "canbaoField": [], "startDateList": [], "capiField": [], "method": "", "keyword": "牛羊肉",
        "sortBy": "", "enableNewSearch": True, "isFirstQuery": True, "page": 1, "hit": 10}
response = requests.post(url=url, headers=headers, data=data).text
print(response)
# for eve_data in response:
#     print(eve_data['originalName'])
