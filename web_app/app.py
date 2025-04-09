"""Flask web application for uploading and displaying analyzed sound events."""

import os
import pymongo
import requests
from flask import Flask, render_template, request, jsonify

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
ml_client_host = os.getenv("ML_CLIENT_HOST", "http://localhost:6000")

app = Flask(__name__)

client = pymongo.MongoClient(mongo_uri)
db = client["sound_analysis"]


@app.route("/")
def index():
    """Render the main dashboard with filtered or recent sound events."""
    filter_type = request.args.get("type")
    query = {"classification": filter_type} if filter_type else {}
    events = list(db.sound_events.find(query).sort("timestamp", -1).limit(20))
    for event in events:
        event["timestamp"] = event["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
    return render_template("index.html", events=events, filter=filter_type)


@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    """Upload and analyze an audio file, returning the classification result."""
    audio = request.files.get("audio")
    if not audio:
        return jsonify({"error": "No audio file uploaded"}), 400

    try:
        response = requests.post(
            f"{ml_client_host}/analyze", files={"audio": audio}, timeout=5
        )
        return jsonify(response.json()), response.status_code
    except ValueError:
        return (
            jsonify(
                {
                    "error": "ML Client did not return valid JSON",
                    "raw_response": response.text,
                }
            ),
            500,
        )
    except requests.RequestException as error:
        return jsonify({"error": f"Failed to connect to ML client: {str(error)}"}), 500

@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    return render_template('add.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
