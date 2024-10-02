# 이벤트 저장이 안됨
# 대충 기능 구현은 되는 것 같은데

from dataiku import app as dataiku_app
from flask import jsonify, request
import dataiku
import os
import json

#app = dataiku_app.FlaskApp()  # Dataiku 웹앱에서 Flask 앱 생성

# 이벤트 데이터를 저장할 파일 경로 설정
EVENTS_FILE_PATH = dataiku.Folder("schedule").get_path() + '/events.json'

# 설비 및 제품 데이터 로드 엔드포인트
@app.route('/get_equipment_and_products', methods=['GET'])
def get_equipment_and_products():
    # equipment 데이터셋 로드
    equipment_dataset = dataiku.Dataset("equipment")
    equipment_df = equipment_dataset.get_dataframe()
    equipment_list = equipment_df.iloc[:, 0].tolist()  # 첫 번째 열이 설비 목록이라고 가정

    # equipment_product 데이터셋 로드
    equipment_products_dataset = dataiku.Dataset("equipment_product")
    equipment_products_df = equipment_products_dataset.get_dataframe()

    # 제품별로 공정 및 설비 데이터 구성
    equipment_products_data = {}
    for product in equipment_products_df['제품'].unique():
        product_data = equipment_products_df[equipment_products_df['제품'] == product]
        processes = product_data.to_dict('records')
        equipment_products_data[product] = processes

    return jsonify({
        'equipmentList': equipment_list,
        'equipmentProductsData': equipment_products_data
    })

# 이벤트 데이터 로드 엔드포인트
@app.route('/load_events', methods=['GET'])
def load_events():
    if os.path.exists(EVENTS_FILE_PATH):
        with open(EVENTS_FILE_PATH, 'r', encoding='utf-8') as f:
            events = json.load(f)
    else:
        events = {}
    return jsonify(events)

# 이벤트 데이터 저장 엔드포인트
@app.route('/save_events', methods=['POST'])
def save_events():
    events = request.get_json()
    with open(EVENTS_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False)
    return 'Success', 200

