import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import os
import multiprocessing as mp
from selenium import webdriver
from time import sleep

def scroll_down(url, waiting_sec):
    dv = webdriver.Chrome()

    dv.get(url)
    dv.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(waiting_sec)

    html = dv.page_source
    soup = BeautifulSoup(html, 'html.parser')

    return [i['href'] for i in soup.select('li[class=goods-form] div[class=prdimg] a')]

def crawl(url, category, codes):
    links = scroll_down(url, 5)
    print(os.getpid(), category, "start")

    cols = ['code', 'new_title', 'contents', 'category', 'price', 'img']
    df = {
        "code": [],
        "new_title": [],
        "contents": [],
        "category": [],
        "price": [],
        "img": []
    }
    cnt = 0
    red = 0

    for i in links:
        code = 'A' + i.split('=')[1]
        if code in codes:
            red += 1
            continue
        url = 'https://attrangs.co.kr' + i
        r = requests.get(url)
        if r.status_code != 200:
            red += 1
            continue
        soup = BeautifulSoup(r.text, 'html.parser')

        title = soup.select('h3[class=name]')
        title = title[0].text if len(title) != 0 else None

        contents = soup.select('p[class=summary]')
        contents = contents[0].text if len(contents) != 0 else None

        price = soup.select('div[class=price] strong')
        price = price[0].text if len(price) != 0 else None

        img = soup.select('div[class=colorbox] img')
        img = img[0]['src'] if len(img) != 0 else None

        for x, y in zip(cols, [code, title, contents, category, price, img]):
            df[x].append(y)
        cnt += 1
        if cnt % 5 == 0:
            print(cnt, '/', len(links), 'redundancy', red)
    
    print(f"total: {cnt} /", len(links), 'redundancy', red)

    df = DataFrame(df).drop_duplicates(['code'])
    df.to_csv('data/' + str(os.getpid()) + '.csv', index=False)



if __name__ == '__main__':
    # 아트랑스 쇼핑몰 기준 니트까지 크롤링 완료
    # 해당하는 주소와 카테고리를 적어서 실행하면 됩니다. n개를 적으면 n개가 병렬로 처리됩니다.
    # 카테고리의 경우 예를 들어 top blouse 의 경우 탑/블라우스 이런 식으로 적기
    # 이 코드가 있는 디렉토리에 attrangs 라는 디렉토리와 chromedriver 가 있어야 합니다.

    src = [
        'https://attrangs.co.kr/shop/list.php?cate=050101',
        'https://attrangs.co.kr/shop/list.php?cate=050102',
        'https://attrangs.co.kr/shop/list.php?cate=050103',
        'https://attrangs.co.kr/shop/list.php?cate=050104'
    ]

    cat = [
        '가방/숄더',
        '가방/지갑',
        '가방/파우치',
        '가방/백팩'
    ]

    procs = []
    #df = pd.read_csv('attrangs/attrangs1.csv')
    #codes = list(df['code'])
    codes = []
    #del df

    for i, j in zip(src, cat):
        p = mp.Process(target=crawl, args=(i, j, codes))
        procs.append(p)
        p.start()
    
    for p in procs:
        p.join()