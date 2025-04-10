[![Web App CI](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/webci.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/webci.yml)
[![Client CI Pipeline](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/client-ci.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/client-ci.yml)
[![lint-free](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/lint.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/lint.yml)

# 🎧 Sound Emotion Dashboard

## 🌟 Project Overview

**Sound Emotion Dashboard** is a full-stack application that allows users to **record live audio** in the browser, **analyze the emotional content** using machine learning models, and receive an **instant song recommendation** that matches the detected mood.

It leverages:

- Real-time browser audio recording  
- Whisper-based transcription and NLP-based emotion classification  
- Flask backend for both web app and ML client  


## 👥 Team Members

- Xiaowei Ma [GitHub](https://github.com/WillliamMa)
- Rishi Rana [GitHub](https://github.com/Rishi-Rana1)
- Mandy Mao [GitHub](https://github.com/manrongm)
- Juno Cheung [Github](https://github.com/avacheungx)


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/software-students-spring2025/4-containers-goldman-stanley.git
cd 4-containers-goldman-stanley
```


### 2. Start the System with Docker

```bash
docker-compose build --no-cache
docker-compose up  
```

Then open the browser and visit:

👉 http://127.0.0.1:5050

## 💡 Demo Use Case

1. Open the app and click "🎙 Start Recording".
2. Say a sentence like: _"I'm feeling very tired and frustrated."_
3. The system will:
   - Record your voice
   - Transcribe the speech using Whisper
   - Detect emotion based on keywords
   - Recommend a matching song
4. Result shown on dashboard:  
   _😊 Emotion: angry_  
   _🎵 Song: Stronger - Kanye West_

