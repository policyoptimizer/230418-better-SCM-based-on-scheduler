import pandas as pd
from flask import Flask, jsonify, request

#app = Flask(__name__)

# Dataiku 라이브러리에서 데이터 읽기
equipment_products_df = pd.read_csv("/home/dataiku/lib/project/project-python-libs/CDS202408221750_heuiy/python/dat/equipment_and_products.csv")
equipment_df = pd.read_csv("/home/dataiku/lib/project/project-python-libs/CDS202408221750_heuiy/python/dat/equipment.csv")

# 제품 리스트 API
@app.route('/get-products', methods=['GET'])
def get_products():
    try:
        product_list = equipment_products_df['제품'].unique().tolist()
        print(f"Loaded products: {product_list}")  # 로깅
        return jsonify({"products": product_list})
    except Exception as e:
        print(f"Error in get_products: {e}")  # 오류 출력
        return jsonify({"error": str(e)}), 500

# 공정 및 설비 리스트 API
@app.route('/get-process-and-equipment', methods=['GET'])
def get_process_and_equipment():
    try:
        product = request.args.get('product')
        process_data = equipment_products_df[equipment_products_df['제품'] == product]
       
        processes = process_data['공정'].tolist()
        equipment1 = process_data['설비1'].tolist()
        equipment2 = process_data['설비2'].dropna().tolist()

        print(f"Product: {product}, Processes: {processes}, Equipment: {equipment1 + equipment2}")  # 로깅
        return jsonify({"processes": processes, "equipment": equipment1 + equipment2})
    except Exception as e:
        print(f"Error in get_process_and_equipment: {e}")  # 오류 출력
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)

