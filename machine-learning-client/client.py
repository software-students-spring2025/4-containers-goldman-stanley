from flask import Flask, request, jsonify
from utils import analyze_audio
import pymongo
import os
from datetime import datetime

app = Flask(__name__)
mongo_uri = os.environ.get("MONGO_URI", "mongodb://mongodb:27017/")
client = pymongo.MongoClient(mongo_uri)
db = client["sound_analysis"]

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['audio']
    audio_data = file.read()

    result = analyze_audio(audio_data)
    result['timestamp'] = datetime.utcnow()
    inserted = db.sound_events.insert_one(result)
    result['_id'] = str(inserted.inserted_id)
    return jsonify({"status": "success", "result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
