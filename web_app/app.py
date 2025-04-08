from flask import Flask, render_template, request, jsonify
from datetime import datetime
import pymongo
import os
import requests

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
ML_CLIENT_HOST = os.getenv("ML_CLIENT_HOST", "http://localhost:6000")

app = Flask(__name__)

client = pymongo.MongoClient(mongo_uri)
db = client["sound_analysis"]

@app.route('/')
def index():
    filter_type = request.args.get("type")
    query = {"classification": filter_type} if filter_type else {}
    events = list(db.sound_events.find(query).sort("timestamp", -1).limit(20))
    for e in events:
        e['timestamp'] = e['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
    return render_template('index.html', events=events, filter=filter_type)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    audio = request.files['audio']

    try:
        response = requests.post(f"{ML_CLIENT_HOST}/analyze", files={'audio': audio})
        return jsonify(response.json()), response.status_code
    except ValueError:
        return jsonify({"error": "ML Client did not return valid JSON", "raw_response": response.text}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to connect to ML client: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)

