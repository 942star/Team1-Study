# ----------------------------
# + Module for Web Crawling  +
# +                          +
# + @date:   2019-07-09      +
# + @author: 한승민            +
# +--------------------------+


import requests
import time
import json
import os
from selenium import webdriver


def download(url, method='get', 
            params=None, data=None, 
            headers = {
                'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
            }, maxretries=4):
    '''
    url에 Request를 보낸 후 그에 대한 Response 객체를 돌려줍니다.
    '''

    try:
        resp = requests.request(method,
                                url,
                                params=params,
                                data=data,
                                headers=headers)
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if 500 <= e.response.status_code < 600 and maxretries > 0:
            print(maxretries)
            resp = download(method, url, params, data, maxretries - 1)
        else:
            print(e.response.status_code)
            print(e.response.reason)
    return resp


def to_html_file(html, filename='result.html', encoding='utf8'):
    '''
    문자열을 filename 위치에 html 파일 형식으로 저장합니다.
    '''

    with open(filename, 'w', encoding=encoding) as file:
        file.write(html)

    print('file path:', os.path.abspath(filename))
    return True


def load_driver(executable_path='driver/chromedriver', options=None, headless=False, *args, **kwargs):
    '''
    정의된 옵션에 따른 Chrome WebDriver 객체를 생성합니다.
    '''

    if options is None:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        # 혹은 options.add_argument("--disable-gpu")
    return webdriver.Chrome(executable_path=executable_path, options=options, *args, **kwargs)
