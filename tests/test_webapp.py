import io
import pytest
from unittest.mock import patch

# Test homepage GET

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sound Emotion Dashboard" in response.data


# Test homepage with filter
@patch("pymongo.collection.Collection.find")
def test_index_filter(mock_find, client):
    mock_find.return_value.sort.return_value.limit.return_value = []
    response = client.get("/?type=speech")
    assert response.status_code == 200
    assert b"Filter by:" in response.data


# Test upload-audio success
@patch("requests.post")
def test_upload_audio_success(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "result": {
            "timestamp": "2025-04-08T12:00:00Z",
            "classification": "speech",
            "energy": 0.1234,
            "emotion": "happy",
            "recommendation": "Happy - Pharrell Williams",
        }
    }
    dummy_audio = io.BytesIO(b"dummy audio")
    dummy_audio.name = "test.webm"
    response = client.post("/upload-audio", data={"audio": dummy_audio}, content_type="multipart/form-data")
    assert response.status_code == 200
    assert response.json["result"]["emotion"] == "happy"


# Test upload-audio ValueError
@patch("requests.post")
def test_upload_audio_invalid_json(mock_post, client):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.side_effect = ValueError("No JSON")
    mock_post.return_value.text = "Not JSON"
    dummy_audio = io.BytesIO(b"dummy audio")
    dummy_audio.name = "test.webm"
    response = client.post("/upload-audio", data={"audio": dummy_audio}, content_type="multipart/form-data")
    assert response.status_code == 500
    assert "raw_response" in response.json

