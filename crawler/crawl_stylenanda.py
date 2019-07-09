from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import os
import multiprocessing as mp
from tqdm import tqdm

def new_title1(n):
    t = n.split("#")
    return t[0]

def new_title2(n):
    t = n.split(" (")
    return t[0]

def crawl(link, category):
    cols = ['code', 'new_title', 'contents', 'category', 'price', 'img']
    data = {}

    for i in cols:
        data[i] = []

    pid = os.getpid()
    print(f"pid: {pid} category: {category} start")
    dv = webdriver.Chrome()
    # dv.add_argument('headless')
    # dv.add_argument('window-size=1920x1080')
    # dv.add_argument("disable-gpu")
    
    dv.get(link)
    
    html = dv.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    links = set([i['href'] for i in soup.select("ul[class='column4'] li a")])
    cnt, total = 0, len(links)
    
    for i in links:
        dv.get('https://stylenanda.com' + i)
    
        text = dv.page_source
        soup = BeautifulSoup(text, 'html.parser')
        
        if len(soup.select('.cont')) == 0:
            continue
        data['contents'].append(soup.select('.cont')[0].text)
        
        title = 0
        code = 0
        for i in soup.select('span'):
            if title and code:
                break
                
            if title:
                # print(i.text)
                data['new_title'].append(i.text)
                title = 0
            if code:
                data['code'].append(i.text)
                code = 0
        
            if i.text == 'Code':
                code = 1
            if i.text == '상품명':
                title = 1
                
        data['price'].append(soup.select("span[class='quantity_price']")[0].text)
        data['img'].append(soup.select('#de_img1 img')[0]['src'])
        data['category'].append(category)

        cnt += 1

        if cnt % 5 == 0 or cnt == total:
            print(f"{category}: {cnt} / {total}")

    final = pd.DataFrame(data)
    final['raw_title'] = list(final['new_title'])
    final['new_title'] = final['new_title'].apply(new_title1)
    final['new_title'] = final['new_title'].apply(new_title2)
    final['contents'] = final['contents'].apply(lambda x:x.replace('\r', ''))
    final['contents'] = final['contents'].apply(lambda x:x.replace('\n', ''))
    final['contents'] = final['contents'].apply(lambda x:' '.join(x.split()))   

    final.to_csv(f'data/{pid}.csv', index=False)

if __name__ == '__main__':
    # 웹드라이버와 py 파일 같은 디렉토리에 있어야 함.

    # 주소
    url = [
        'https://stylenanda.com/product/list.html?cate_no=404'
        # 'https://stylenanda.com/product/list.html?cate_no=406',
        # 'https://stylenanda.com/product/list.html?cate_no=403'
    ]

    # 카테고리 이름
    cat = [
        '슈즈/플랫,로퍼'
        # '슈즈/부츠,부티',
        # '슈즈/샌들,슬리퍼'
    ]
    procs = []

    for i, j in zip(url, cat):
        p = mp.Process(target=crawl, args=(i, j))
        procs.append(p)
        p.start()
    
    for p in procs:
        p.join()