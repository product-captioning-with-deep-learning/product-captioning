import numpy as np
import torch
import pickle


MAX_SEQ_LEN = 30
path_corpus = 'mydata/result.txt'


def load_vec(path):
    # 미리 저장된 word embedding matrix 로드
    f = open(path, encoding='utf-8')
    f.readline()

    vec = dict()
    cnt = 0
    for i in range(30185):
        inp = f.readline().split()
        emb_vec = [float(x) for x in inp[-200:]]
        vec[inp[1]] = emb_vec
        cnt += 1
        
    f.close()
    print(len(vec))

    return vec

def make_mapping(corpus):
    # 인덱스와 단어 사이 매핑 만들기

    words = set()
    word2idx = {
        '<start>': 0,
        '<unk>': 1
    }
    idx2word = {
        0: '<start>',
        1: '<unk>'
    }

    idx = 2
    for sentence in corpus:
        for word in sentence:
            if word == None:
                continue
            words.add(word)
        
    for word in words:
        if word == '사이즈':
            print(word)
        word2idx[word] = idx
        idx2word[idx] = word
        idx += 1
    
    return word2idx, idx2word


def make_real_data(corpus, word2idx, seq_len):
    #seq len 씩 끊어서 저장
    real_data = []
    for sentence in corpus:
        j = [0]
        for word in sentence:
            if word == '.' or word == None:
                continue
            j.append(word2idx[word])

        real_data.extend(j)
    
    return [real_data[i:i + seq_len] for i in range(0, len(real_data) - seq_len, seq_len)]


# 데이터 잘 들어왔는지 확인
def check_data():
    real_data = pickle.load(open('./mydata/real_data.txt', 'rb'))   # real_data
    emb_mat = pickle.load(open('./mydata/word2vec.txt', 'rb'))    # embedding matrix
    vocab_to_int = pickle.load(open('./mydata/word2idx.txt', 'rb')) # vocab to int
    int_to_vocab = pickle.load(open('./mydata/idx2word.txt', 'rb')) # int to vocab

    print(len(real_data[-1]), len(real_data))
    print(emb_mat[-1], len(emb_mat))
    print(vocab_to_int['<start>'], len(vocab_to_int))
    print(int_to_vocab[0], len(int_to_vocab))

# 각 문장을 tokenizing 한 데이터 로드
corpus = pickle.load(open(path_corpus), 'rb')
print(corpus[:5])

word2idx, idx2word = make_mapping(corpus)

vec_ref = load_vec('embed/vec.txt')
word2vec = dict()

print('word2idx', len(word2idx))

hit, miss = 0, 0

for i in word2idx:
    if i in vec_ref:
        hit += 1
    else:
        miss += 1
    word2vec[i] = vec_ref[i] if i in vec_ref else list(np.random.randn(200))

print('총 단어 수:', len(word2vec))
print('hit', hit, 'miss', miss)

rd = make_real_data(corpus, word2idx, MAX_SEQ_LEN)

emb_mat = [[] for i in range(len(word2vec))]
for i in word2vec:
    emb_mat[word2idx[i]] = word2vec[i]

pickle.dump(emb_mat, open('mydata/word2vec.txt', 'wb'))
pickle.dump(word2idx, open('mydata/word2idx.txt', 'wb'))
pickle.dump(idx2word, open('mydata/idx2word.txt', 'wb'))
pickle.dump(rd, open('mydata/real_data.txt', 'wb'))

# check_data()