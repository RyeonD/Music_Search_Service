# 노래 제목으로 검색 시 실행 - 해당 제목을 가진 노래의 가사를 분석. 비슷한 가사를 가진 노래 반환
import urllib.request
import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import gensim
import os
from konlpy.tag import Okt

df_path = '../data/title_analytics/music.csv'

# 입력값 토큰화
def tokenize_for_title(text):
    okt = Okt()
    word_s = okt.pos(text)
    result = []
    for n, h in word_s:
        # if h == 'Josa': continue
        result.append(n)
    return result

# 입력 텍스트에서 가장 많은 데이터를 포함하는 데이터프레임 추출
def getSongIndex(df, text): 
    result = None
    tokenized_text = tokenize_for_title(text)

    for i in tokenized_text :
        if result is None :
            result = df[df['name'].str.contains(i)]
        else:
            result = result[result['name'].str.contains(i)]
    return result.index.values[0]

# 연도별 모든 csv 데이터 하나로 합쳐서 파일 저장
def init() :
    path = '../data/year_music_info/'
    df1 = pd.read_csv(path + "final_1960s_info_v3.csv", encoding='utf-8', index_col = 0)
    df2 = pd.read_csv(path + "final_1970s_info_v3.csv", encoding='utf-8', index_col = 0)
    df3 = pd.read_csv(path + "final_1980s_info_v3.csv", encoding='utf-8', index_col = 0)
    df4 = pd.read_csv(path + "final_1990s_info_v3.csv", encoding='utf-8', index_col = 0)
    df5 = pd.read_csv(path + "final_2000s_info_v3.csv", encoding='utf-8', index_col = 0)
    df6 = pd.read_csv(path + "final_2010s_info_v3.csv", encoding='utf-8', index_col = 0)

    frames = [df1,df2,df3,df4,df5,df6]
    result = pd.concat(frames)
    result

    df_None = result[result['lyrics']=='None'].index
    df = result.drop(df_None)
    df = df.reset_index(drop=True)

    rename_list = []
    for i in range(len(df)):
        rename_list.append(df.name[i].strip())
    df['name'] = rename_list

    df.to_csv('../data/title_analytics/music.csv')

# csv 없으면 새로 만듬
def knock_knock() :
    if os.path.isfile(df_path) :
        pass
    else :
        init()

def first() :
    knock_knock() # 읽어올 csv 확인
    df = pd.read_csv(df_path, index_col= 0)
    corpus = []
    for words in df['lyrics']:
        corpus.append(words.split())

    # 사전 훈련된 워드 임베딩 활용
    ko_model = gensim.models.Word2Vec.load('../data/title_analytics/ko/ko.bin')
    ko_model.train(corpus, total_examples = ko_model.corpus_count, epochs = 15)
    return df, ko_model

def vectors(document_list, ko_model):
    document_embedding_list = []

    # 각 문서에 대해서
    for line in document_list:
        doc2vec = None
        count = 0
        for word in line.split():
            if word in ko_model.wv.vocab:
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더함
                if doc2vec is None:
                    doc2vec = ko_model[word]
                else:
                    doc2vec = doc2vec + ko_model[word]

        if doc2vec is not None:
            # 단어 벡터를 모두 더한 벡터의 값을 문서 길이로 나눠줌
            doc2vec = doc2vec / count
            document_embedding_list.append(doc2vec)

    # 각 문서에 대한 문서 벡터 리스트를 리턴
    return document_embedding_list

def recommendations(name):
    df, ko_model = first()

    document_embedding_list = vectors(df['lyrics'], ko_model)
    print('문서 벡터의 수 :',len(document_embedding_list))

    cosine_similarities = cosine_similarity(document_embedding_list, document_embedding_list)
    print('코사인 유사도 매트릭스의 크기 :',cosine_similarities.shape)

    # 노래의 제목을 입력하면 해당 제목의 인덱스를 리턴받아 idx에 저장
    # indices = pd.Series(df.index, index = df['name']).drop_duplicates()
    # idx = indices[name]
    idx = getSongIndex(df, name)
    print(idx)

    # 입력된 노래 가사(document embedding)가 유사한 노래 5개 선정
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:31]

    # 가장 유사한 음악 5개의 인덱스
    music_indices = [i[0] for i in sim_scores]
    
    result = df.iloc[music_indices]
    result.drop('lyrics', axis = 1, inplace = True)
    result.reset_index(drop = True, inplace = True)
    
    js = result.to_json(orient = 'split', force_ascii=False)

    return js
    
    # music = df[['name', 'img']]
    
    # 전체 데이터프레임에서 해당 인덱스의 행만 추출. 5개의 행을 가진다.
    # recommend = music.iloc[music_indices].reset_index(drop=True)
    # name, img
    
    # fig = plt.figure(figsize=(20, 30))

    # 데이터프레임으로부터 순차적으로 이미지를 출력
    # for index, row in recommend.iterrows():
    #     response = requests.get(row['img'])
    #     img = Image.open(BytesIO(response.content))
    #     fig.add_subplot(5, 6, index + 1)
    #     plt.imshow(img)
    #     path= 'C:/Users/user/쥬피터 작업 파일/semi-project/final_since_info_v2/NanumBarunGothic.ttf'
    #     fontprop = fm.FontProperties(fname=path, size=10)
    #     plt.title(row['name'], fontproperties=fontprop)
