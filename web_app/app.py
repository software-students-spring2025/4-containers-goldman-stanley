from flask import Flask, render_template, request
import pymongo
from datetime import datetime
import os

app = Flask(__name__)

mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
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

if __name__ == '__main__':
    print("Starting Flask app on 0.0.0.0:5000...")
    app.run(host='0.0.0.0', port=5050)