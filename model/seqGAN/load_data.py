import numpy as np
import torch
import pickle


MAX_SEQ_LEN = 30

def load_vec(path):
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

def make_real_data(corpus, word2idx, seq_len):
    #seq len 씩 끊어서 저장
    real_data = []
    for i in corpus:
        j = []
        for word in i:
            if word == '.' or word == None:
                continue
            j.append(word2idx[word])

        # seq_len 과 길이가 다를 경우 제외
        if len(j) == seq_len:
            real_data.extend(j)
        else:
            continue
    
    return [real_data[i:i + seq_len] for i in range(0, len(real_data) - seq_len, seq_len)]


# 데이터 잘 들어왔는지 확인

# real_data = pickle.load(open('./mydata/real_data.txt', 'rb'))   # real_data
# emb_mat = pickle.load(open('./mydata/word2vec.txt', 'rb'))    # embedding matrix
# vocab_to_int = pickle.load(open('./mydata/word2idx.txt', 'rb')) # vocab to int
# int_to_vocab = pickle.load(open('./mydata/idx2word.txt', 'rb')) # int to vocab

# print(len(real_data[-1]), len(real_data))
# print(emb_mat[-1], len(emb_mat))
# print(vocab_to_int['사이즈'], len(vocab_to_int))
# print(int_to_vocab[0], len(int_to_vocab))
# exit()

# corpus 로드
corpus = pickle.load(open('mydata/result.txt', 'rb'))
print(corpus[:5])

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
        if word == '.' or word == None:
            continue
        words.add(word)
    
for word in words:
    if word == '사이즈':
        print(word)
    word2idx[word] = idx
    idx2word[idx] = word
    idx += 1

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

emb_mat = [[] for i in range(0, len(word2vec))]
for i in word2vec:
    emb_mat[word2idx[i]] = word2vec[i]

pickle.dump(emb_mat, open('mydata/word2vec.txt', 'wb'))
pickle.dump(word2idx, open('mydata/word2idx.txt', 'wb'))
pickle.dump(idx2word, open('mydata/idx2word.txt', 'wb'))
pickle.dump(rd, open('mydata/real_data.txt', 'wb'))