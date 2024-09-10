import dataiku
import json

# 폴더 설정
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
        return jsonify({}), 200
