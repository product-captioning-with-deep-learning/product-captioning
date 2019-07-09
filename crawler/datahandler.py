import pandas as pd
import re
import torch
import pickle


def sn_clear(name):
    # 스타일난다 전처리
    
    sn = pd.read_csv(name)

    sn['contents'] = sn['contents'].apply(lambda x:x.replace('\r', ''))
    sn['contents'] = sn['contents'].apply(lambda x:x.replace('\n', ''))
    sn['contents'] = sn['contents'].apply(lambda x:' '.join(x.split()))
    sn.to_csv('stylenanda.csv', index=False)

def att_clear(name):
    #아트랑스 전처리

    att = pd.read_csv(name)
    att['contents'] = att['contents'].apply(lambda x:x if str(x) == 'nan' or x.split()[0][0] != '(' else ' '.join(x.split()[1:]))

    att.to_csv('attrangs1.csv', index=False)

def remove_sc(name):
    # 특수문자 제거

    hangul = re.compile('[^ ㄱ-ㅣ가-힣,.]+')
    df = pd.read_csv(name)
    df['contents'] = df['contents'].apply(lambda x: x if str(x) == 'nan' else hangul.sub('', x))

    df.to_csv(name,index=False)

def make_corpus(name):
    # 문장단위로 끊기

    df = pd.read_csv(name + '.csv', encoding='utf-8')
    df = df[df['contents'].notnull()]
    corpus = []
    for i in df['contents']:
        for sentence in i.split('.'):
            corpus.append(sentence)

    return corpus