"""Unit tests for the Flask web app endpoints."""

import io
from unittest.mock import patch

def test_index(client):
    """Test the home page loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sound Emotion Dashboard" in response.data


@patch("pymongo.collection.Collection.find")
def test_index_filter(mock_find, client):
    """Test the filter functionality on the homepage."""
    mock_find.return_value.sort.return_value.limit.return_value = []
    response = client.get("/?type=speech")
    assert response.status_code == 200
    assert b"Filter by:" in response.data


@patch("requests.post")
def test_upload_audio_success(_, client):
    """Test successful upload and analysis of audio."""
    _.return_value.status_code = 200
    _.return_value.json.return_value = {
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
    response = client.post(
        "/upload-audio", data={"audio": dummy_audio}, content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert response.json["result"]["emotion"] == "happy"


@patch("requests.post")
def test_upload_audio_invalid_json(_, client):
    """Test response when ML client returns invalid JSON."""
    _.return_value.status_code = 200
    _.return_value.json.side_effect = ValueError("No JSON")
    _.return_value.text = "Not JSON"
    dummy_audio = io.BytesIO(b"dummy audio")
    dummy_audio.name = "test.webm"
    response = client.post(
        "/upload-audio", data={"audio": dummy_audio}, content_type="multipart/form-data"
    )
    assert response.status_code == 500
    assert "raw_response" in response.json


@patch("requests.post", side_effect=Exception("Connection refused"))
def test_upload_audio_exception(_, client):
    """Test upload-audio route handles connection exceptions."""
    dummy_audio = io.BytesIO(b"dummy audio")
    dummy_audio.name = "test.webm"
    response = client.post(
        "/upload-audio", data={"audio": dummy_audio}, content_type="multipart/form-data"
    )
    assert response.status_code == 500
    assert "Failed to connect" in response.json["error"]
