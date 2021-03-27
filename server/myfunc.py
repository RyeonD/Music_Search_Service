import random as r
import pandas as pd
import os

pwd = os.getcwd()

# internal ===================================== #

# 가사를 제외한 년도 데이터 읽어오기
def readData(since, count) :
    df = pd.read_csv(f'../data/year_music_info/final_{since}s_info_v3.csv', index_col=0)
    df.drop('lyrics', axis = 1, inplace = True) # 가사는 필요없으니 지우지만 필요하면 쓰기!
    index = df.index.values.tolist()
    rand_indexes = r.sample(index, count)
    data = df.loc[rand_indexes]
    return data

# external ===================================== #

# 라벨에 따라 년도 나누기
def sliceLabel(label, no) :
    n1, n2 = label[:2], label[2:]
    year = '19' if no != 2 else '20' # no가 2면 2000년 아니면 1900년
    return year + n1, year + n2

# csv 읽어와 곡 정보 반환
def read_randomData(since1, since2 = None):
    df_list = [since1, since2] # 일단 인자값으로 리스트생성
    count = 30     if since2 is None else 15 # since2가 None 아니면 15
    stop_range = 1 if since2 is None else 2  # 이하 동문
    data = None

    # 반복을 한번 이상하면 병합작업을 거침
    for i in list(range(0, stop_range, 1)) :
        print(df_list[i])
        temp = readData(df_list[i], count)
        data = pd.concat([data, temp])

    js = data.to_json(orient = 'split', force_ascii=False)
    
    return js