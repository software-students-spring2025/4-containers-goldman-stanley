"""Utilities for analyzing audio and recommending music based on detected emotion."""

import io
import os
import uuid
import wave

import numpy as np
import whisper
from pydub import AudioSegment

KEYWORD_EMOTION_MAP = {
    "love": "happy",
    "thank": "happy",
    "great": "happy",
    "awesome": "excited",
    "wow": "excited",
    "amazing": "excited",
    "tired": "calm",
    "quiet": "calm",
    "boring": "neutral",
    "fine": "neutral",
    "sad": "sad",
    "angry": "angry",
    "frustrated": "angry",
}

SONG_RECOMMENDATIONS = {
    "calm": "Weightless - Marconi Union",
    "neutral": "Let Her Go - Passenger",
    "happy": "Happy - Pharrell Williams",
    "excited": "Can't Stop the Feeling! - Justin Timberlake",
    "sad": "Someone Like You - Adele",
    "angry": "Stronger - Kanye West",
}

model = whisper.load_model("base")  # pylint: disable=invalid-name


def extract_transcript(audio_path):
    """Transcribes the given audio file and returns lowercase text."""
    try:
        result = model.transcribe(audio_path)
        return result["text"].lower()
    except Exception:  # pylint: disable=broad-exception-caught
        return ""


def infer_emotion_from_text(text):
    """Infers emotion from keywords in the given text."""
    for word in text.split():
        for keyword, emotion in KEYWORD_EMOTION_MAP.items():
            if keyword in word:
                return emotion
    return "neutral"


def analyze_audio(audio_bytes):
    """
    Analyzes audio bytes, classifies speech vs silence,
    infers emotion from speech, and recommends a song.
    """
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="webm")
    wav_io = io.BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    temp_filename = f"temp_{uuid.uuid4().hex}.wav"
    with open(temp_filename, "wb") as audio_file:
        audio_file.write(wav_io.read())
    wav_io.seek(0)

    with wave.open(wav_io, "rb") as wave_file:
        n_channels = wave_file.getnchannels()
        frames = wave_file.readframes(wave_file.getnframes())

    samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    samples /= np.iinfo(np.int16).max
    if n_channels > 1:
        samples = samples[::n_channels]

    energy = float(np.sqrt(np.mean(samples**2)))
    classification = "speech" if energy > 0.02 else "silence"

    if classification == "speech":
        transcript = extract_transcript(temp_filename)
        emotion = infer_emotion_from_text(transcript)
    else:
        emotion = "calm"

    os.remove(temp_filename)
    song = SONG_RECOMMENDATIONS.get(emotion, "Let Her Go - Passenger")

    return {
        "classification": classification,
        "energy": round(energy, 4),
        "emotion": emotion,
        "recommendation": song,
    }
