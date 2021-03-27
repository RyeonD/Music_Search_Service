#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# tfidf.py
# TF-IDF로 텍스트를 벡터로 변환하는 모듈 - tdidf.py로 저장
from konlpy.tag import Okt
import pickle
import numpy as np

# KoNLPy의 Okt객체 초기화 
okt = Okt()

# 전역 변수 
word_dic = {'_id': 0} # 단어 사전
dt_dic = {} # 문장 전체에서의 단어 출현 횟수
files = [] # 문서들을 저장할 리스트
texts = []

def start():
    global word_dic
    word_dic = {'_id': 0}
    global dt_dic
    dt_dic = {}
    global files
    files = []
    texts = []

## 조사만 제거
def tokenize(text):
    result = []
    word_s = okt.pos(text)
    for n, h in word_s:
        if h == 'Josa': continue
        result.append(n)
    return result


'''
## 명사,형용사 동사만 뽑고 정규화, 근어화
def tokenize(text):
    result = []
    word_s = okt.pos(text, norm=True, stem=True)
    for n, h in word_s:
        if not (h in ['Noun', 'Verb ', 'Adjective']): continue
        if h == 'Josa': continue
        result.append(n)
    return result
'''
'''
## 2글자 이상 명사만 뽑기
def tokenize(text):
    result = []
    word_s = okt.pos(text)
    for n, h in word_s:
        if not (h in ['Noun']): continue
        if h == 'Josa': continue
        if len(n)> 1:
            result.append(n)
    return result
'''


def words_to_ids(words, auto_add = True):
    ''' 단어를 ID로 변환하기 ''' 
    result = []
    for w in words:
        if w in word_dic:
            result.append(word_dic[w])
            continue
        elif auto_add:
            id = word_dic[w] = word_dic['_id']
            word_dic['_id'] += 1
            result.append(id)
    return result

def add_text(text):
    '''텍스트를 ID 리스트로 변환해서 추가하기''' 
    ids = words_to_ids(tokenize(text))
    files.append(ids)
    texts.append(tokenize(text))

def add_file(path):
    '''텍스트 파일을 학습 전용으로 추가하기''' 
    with open(path, "r", encoding="utf-8") as f:
        s = f.read()
        add_text(s)

def calc_files():
    '''추가한 파일 계산하기''' 
    global dt_dic
    result = []
    doc_count = len(files)
    dt_dic = {}
    
    # 단어 출현 횟수 세기 
    for words in files:
        used_word = {}
        data = np.zeros(word_dic['_id'])
        for id in words:
            data[id] += 1
            used_word[id] = 1
        # 단어 t가 사용되고 있을 경우 dt_dic의 수를 1 더하기 
        for id in used_word:
            if not(id in dt_dic): dt_dic[id] = 0
            dt_dic[id] += 1
        # 정규화하기 
        data = data / len(words) 
        result.append(data)
        
    # TF-IDF 계산하기 
    for i, doc in enumerate(result):
        for id, v in enumerate(doc):
            idf = np.log(doc_count / dt_dic[id]) + 1
            doc[id] = min([doc[id] * idf, 1.0])
        result[i] = doc
    return result

def save_dic(fname):
    '''사전을 파일로 저장하기''' 
    pickle.dump(
        [word_dic, dt_dic, files],
        open(fname, "wb"))

def load_dic(fname):
    '''사전 파일 읽어 들이기''' 
    global word_dic, dt_dic, files
    n = pickle.load(open(fname, 'rb'))
    word_dic, dt_dic, files = n

def calc_text(text):
    ''' 문장을 벡터로 변환하기 ''' 
    data = np.zeros(word_dic['_id'])
    words = words_to_ids(tokenize(text), False)
    for w in words:
        data[w] += 1
    data = data / len(words)
    for id, v in enumerate(data):
        idf = np.log(len(files) / dt_dic[id]) + 1
        data[id] = min([data[id] * idf, 1.0])
    return data

#%%

# 모듈 테스트하기 
if __name__ == '__main__':
    add_file('./text/2000/lyrics_test4077.txt')
    print(calc_files())
    print(word_dic)
    
#%%

tokenize('나는 오늘 비가 피자 머리입니다.')
