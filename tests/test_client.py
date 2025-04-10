import io
import pytest
import numpy as np
from unittest.mock import patch, MagicMock

import sys
import os
import types

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import machine_learning_client.utils
sys.modules['utils'] = machine_learning_client.utils
utils = machine_learning_client.utils
from machine_learning_client.client import app


dummy_audio = b"dummy audio content"

@patch("machine_learning_client.client.analyze_audio")
@patch("machine_learning_client.client.db")
def test_analyze_success(mock_db, mock_analyze_audio):
    mock_analyze_audio.return_value = {
        "classification": "speech",
        "energy": 0.03,
        "emotion": "happy",
        "recommendation": "Happy - Pharrell Williams"
    }
    mock_db.sound_events.insert_one.return_value.inserted_id = "mocked_id"

    test_client = app.test_client()
    data = {"audio": (io.BytesIO(dummy_audio), "test.webm")}
    response = test_client.post("/analyze", data=data, content_type="multipart/form-data")

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "success"
    assert json_data["result"]["emotion"] == "happy"
    assert json_data["result"]["_id"] == "mocked_id"



def test_analyze_no_audio():
    test_client = app.test_client()
    response = test_client.post("/analyze", data={}, content_type="multipart/form-data")
    assert response.status_code == 400
    assert response.get_json() == {"error": "No file part"}


def test_infer_emotion_from_text_known():
    text = "I feel awesome today"
    assert utils.infer_emotion_from_text(text) == "excited"


def test_infer_emotion_from_text_unknown():
    text = "blabla randomness"
    assert utils.infer_emotion_from_text(text) == "neutral"


@patch("machine_learning_client.utils.model.transcribe")
def test_extract_transcript_success(mock_transcribe):
    mock_transcribe.return_value = {"text": "This is great"}
    result = utils.extract_transcript("fake_path.wav")
    assert result == "this is great"


@patch("machine_learning_client.utils.model.transcribe", side_effect=Exception("fail"))
def test_extract_transcript_fail(_):
    result = utils.extract_transcript("invalid_path.wav")
    assert result == ""


@patch("machine_learning_client.utils.AudioSegment.from_file")
@patch("machine_learning_client.utils.extract_transcript", return_value="I am sad")
def test_analyze_audio_speech(mock_transcript, mock_audio):
    mock_segment = MagicMock()
    mock_segment.export = MagicMock()
    mock_audio.return_value = mock_segment

    with patch("machine_learning_client.utils.wave.open") as mock_wave:
        wave_obj = MagicMock()
        wave_obj.getnchannels.return_value = 1
        wave_obj.getsampwidth.return_value = 2
        wave_obj.getnframes.return_value = 100
        wave_obj.readframes.return_value = np.random.randint(-32768, 32767, 100, dtype=np.int16).tobytes()
        mock_wave.return_value.__enter__.return_value = wave_obj

        result = utils.analyze_audio(b"fake-audio")
        assert result["classification"] == "speech"
        assert result["emotion"] == "sad"
        assert "recommendation" in result


@patch("machine_learning_client.utils.AudioSegment.from_file")
def test_analyze_audio_silence(mock_audio):
    mock_segment = MagicMock()
    mock_segment.export = MagicMock()
    mock_audio.return_value = mock_segment

    with patch("machine_learning_client.utils.wave.open") as mock_wave:
        wave_obj = MagicMock()
        wave_obj.getnchannels.return_value = 1
        wave_obj.getsampwidth.return_value = 2
        wave_obj.getnframes.return_value = 100
        wave_obj.readframes.return_value = (np.zeros(100, dtype=np.int16)).tobytes()
        mock_wave.return_value.__enter__.return_value = wave_obj

        result = utils.analyze_audio(b"fake-audio")
        assert result["classification"] == "silence"
        assert result["emotion"] == "calm"
