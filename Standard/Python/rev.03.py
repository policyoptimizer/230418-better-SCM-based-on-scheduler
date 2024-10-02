from flask import request, jsonify
import dataiku
import json

# Dataiku에서 제공하는 webapp 객체 사용

# 폴더 설정 (Dataiku의 폴더 ID를 사용해야 합니다)
folder = dataiku.Folder("calendar")

# 저장 로직
def save_events():
    events = request.json
    with folder.get_writer("event_backup.json") as writer:
        writer.write(json.dumps(events).encode('utf-8'))
    return 'Success', 200

webapp.add_route('/load-events', 'POST', save_events)

# 로드 로직
def load_events():
    try:
        with folder.get_download_stream("event_backup.json") as stream:
            events = json.loads(stream.read().decode('utf-8'))
        return jsonify(events)
    except:
        return jsonify([]), 200

webapp.add_route('/load-events', 'GET', load_events)
