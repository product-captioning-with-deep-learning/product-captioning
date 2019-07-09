import pandas as pd
import urllib.request
import os

# csv 파일에 각 이미지의 url 이 저장 되어 있다.
# 이를 이용하여 이미지 저장
# 한꺼번에 이미지를 다운 받으면 멈추는 현상이 발생해 batch_size 만큼 끊어서 다운 받기
# 한꺼번에 이미지를 다운 받고 싶으면 batch size 를 큰 값으로 설정

filename = 'final.csv'
batch_size = 100
path = 'img/'
imgtype = '.jpg'


df = pd.read_csv(filename)
df = df[df['img'].notnull()]
total = len(df['code'])

stage = 0
start, end = batch_size * stage, min(batch_size * (stage + 1), total)
print(start, end)

cnt = start
total = len(df['code'])
for i, j in zip(df['img'][start:end], df['code'][start:end]):
    if i == 'https:nan':
        continue
    urllib.request.urlretrieve(i, path + str(j) + imgtype)
    cnt += 1
    if cnt % 10 == 0:
        print(cnt, '/', total)
