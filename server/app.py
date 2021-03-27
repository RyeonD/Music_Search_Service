from flask import Flask, request, jsonify, render_template
import requests
import json
import myfunc as m 
import lyrics_anlytics as la
import title_analyrics as title_analy
app = Flask(__name__)

# main page load
@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

# 입력 받은 가사의 분석결과(비슷한 시대)의 노래들의 정보를 반환
@app.route('/lyrics', methods=['GET'])
def getLyricsByClient():
    lyrics = request.args['data']
    
    # label : 라벨(년도), per : 정확도 (%), no : 6070 = 0, 8090 = 1, 0010 = 2
    label, per, no = la.lyrics_check(lyrics) 
    per = str(round(float(per), 4))

    # 년도 반환
    since1, since2 = m.sliceLabel(label, no)

    # 반환 받은 년도와 csv 내의 데이터를 랜덤으로 30개 내보내기
    result = {'since': [since1,since2], 'data': json.loads(m.read_randomData(since1, since2))}
    return result

# 입력 받은 제목의 노래 가사의 분석결과(비슷한 가사의 노래들)의 정보를 반환
@app.route('/title', methods=['GET'])
def getTitleByClient():
    title = request.args['data']
    
    data = title_analy.recommendations(title) # 전체 노래데이터에서 json처리된 DataFrame 반환됨
    
    return data

# flask 실행(port:9201)
if __name__ == '__main__':
    app.run(port = '9201', debug=True)