![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)
[![log github events](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/event-logger.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/event-logger.yml)
[![Client CI Pipeline](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/client-ci.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/client-ci.yml)
[![Web App CI](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/webci.yml/badge.svg)](https://github.com/software-students-spring2025/4-containers-goldman-stanley/actions/workflows/webci.yml)

# Sound Emotion Dashboard

## Project Description
The Sound Emotion Dashboard is an interactive web application that analyzes audio recordings to detect emotions and provides song recommendations based on the detected emotion. The system classifies audio inputs as either speech or silence, measures energy levels, determines the emotional content, and suggests music that matches the detected mood.

This project combines web development with machine learning to create a user-friendly interface for audio emotion analysis. Users can record audio directly through the browser, submit it for analysis, and view a dashboard of past recordings with their associated emotional classifications and music recommendations.

## Team Members
- [Juno Cheung](https://github.com/avacheungx)
- [William Ma](https://github.com/WillliamMa)
- [Rishi Rana](https://github.com/Rishi-Rana1)
- [Mandy Mao](https://github.com/manrongm)

## System Architecure

1. **Web Application (Flask)**: Handles the user interface, audio recording, and displays analysis results

2. **ML Client**: Processes audio files and performs emotion analysis (separate service)

## Prerequisites

- **Python**: 3.10 or higher
- **Docker**: Latest Version
- **MongoDB**: 4.4 or higher
- Web Browser with access to a micophone

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/software-students-spring2025/4-containers-goldman-stanley.git

cd 4-containers-goldman-stanley
```

### 2. Set up Docker Enviornment

```bash
# Build and start all services using Docker Compose
docker-compose up -d

# To view logs
docker-compose logs -f

# To stop all services
docker-compose down
```

## Running the Application

### 1. Start the Docker Containers

From the root directory of the project:

```bash
docker-compose up -d
```

This will start all services (web application, ML client, and MongoDB) in the background.

To see the logs in real-time:

```bash
docker-compose logs -f
```

If you need to rebuild containers after making changes:

```bash
docker-compose up -d --build
```

### 2. Access the Application

Open your browser and navigate to:
```
http://localhost:5050
```

You should see the Sound Emotion Dashboard with:
- A header showing "🎧 Sound Emotion Dashboard"
- A filter dropdown to filter events by type
- A "Record Now!" button to add new sound events
- A grid displaying past sound events (if any exist in the database)

### 3. Recording and Analyzing Sound

1. Click the "Record Now!" button
2. Allow browser access to your microphone when prompted
3. Click "Start Recording" and speak into your microphone
4. Click "Stop Recording" when finished
5. Choose "Confirm" to submit the recording for analysis or "Cancel" to discard
6. After processing, you'll be redirected to the dashboard where your analyzed recording will appear

### 4. Stopping the Application

When you're done using the application:

```bash
docker-compose down
```

To completely remove volumes (including the MongoDB data):

```bash
docker-compose down -v
```
