import requests


def get_picture():
    word_list = []
    for word in word_list:
        url = "https://www.google.com/search?"
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4636.4 Safari/537.36"
        }
        params = {
            'q': word,
            'tbm': 'isch',
            'hl': 'zh-CN',
            'tbs': '',
            'sa': 'X',
            'ved': '0CAEQpwVqFwoTCNCW1uKuj_QCFQAAAAAdAAAAABAC',
            'biw': '1903',
            'bih': '969',
        }
