from flask import request, jsonify
import dataiku
import json

# Dataiku에서 제공하는 app 객체 사용 (app = Flask(__name__) 제거)

# 폴더 설정 (Dataiku의 폴더 ID를 사용해야 합니다)
folder = dataiku.Folder("calendar")

# 저장 로직
@app.route('/save-events', methods=['POST'])
def save_events():
    events = request.json
    with folder.get_writer("event_backup.json") as writer:
        writer.write(json.dumps(events).encode('utf-8'))
    return 'Success', 200

# 로드 로직
@app.route('/load-events', methods=['GET'])
def load_events():
    try:
        with folder.get_download_stream("event_backup.json") as stream:
            events = json.loads(stream.read().decode('utf-8'))
        return jsonify(events)
    except:
        return jsonify([]), 200

# Dataiku에서는 app.run()을 호출하지 않습니다.

