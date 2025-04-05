import time
import datetime
import sounddevice as sd
import numpy as np
import pymongo
from utils import classify_sound

def record_audio(duration=2, fs=44100):
    print("Recording audio...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    return audio.flatten()

def save_to_db(result, db):
    db.sound_events.insert_one({
        "timestamp": datetime.datetime.utcnow(),
        "classification": result["label"],
        "energy": result["energy"],
        "mean_freq": result["mean_freq"]
    })

if __name__ == '__main__':
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["sound_analysis"]

    while True:
        audio = record_audio()
        result = classify_sound(audio)
        save_to_db(result, db)
        print(f"Saved: {result}")
        time.sleep(5)