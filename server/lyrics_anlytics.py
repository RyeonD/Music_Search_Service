# 가사 입력시 실행 - 가사 분석 및 유사도 높은 년도와 노래 반환
import pickle, tfidf
import numpy as np
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.models import model_from_json

# 모델 정의하고 가중치 데이터 불러오기
nb_classes = 3
model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(38619,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(nb_classes, activation='softmax'))
model.compile(
    loss='categorical_crossentropy',
    optimizer=RMSprop(),
    metrics=['accuracy'])
model.load_weights('../data/lyrics_analytics/text/lyrics2-model.hdf5')
global word_dic, dt_dic, files

# TF-IDF 사전 읽기
c = tfidf.load_dic("../data/lyrics_analytics/text/lyrics2-tfidf.dic")

def lyrics_check(text):
    # 레이블 정의하기
    LABELS = ["6070","8090","0010"]
    # TF-IDF 벡터로 변환하기 
    data = tfidf.calc_text(text)
    # MLP로 예측하기 
    pre = model.predict(np.array([data]))[0]
    n = pre.argmax()
    # print(pre)
    # print(LABELS[n], "(", pre[n], ")")
    return LABELS[n], float(pre[n]), int(n) 

# 인터프리터에서 해당 파이썬을 로드할 때. 아래 코드를 실행하겠다는 조건.
# 조건을 안주거나 else로 빼면 모듈로 사용
# if __name__ == '__main__': 
#     lyrics_check(sunset_old)
#     lyrics_check(sunset_new)