#!/bin/bash

echo "🚀 Setting up Codespace..."

# Install Python deps
pip install --upgrade pip
pip install -r machine_learning_client/requirements.txt
pip install -r web_app/requirements.txt

# Start MongoDB in background
sudo apt update && sudo apt install -y mongodb
sudo service mongodb start
echo "✅ MongoDB started"

# Set ENV VARs
export MONGO_URI="mongodb://localhost:27017/"
export ML_CLIENT_HOST="http://localhost:6000"

# Run ML client in background
echo "🎧 Starting ML Client..."
python3 machine_learning_client/client.py &

# Run Flask App (you can Ctrl+C it and run again manually if needed)
echo "🌐 Starting Flask Web App on port 5050..."
cd web_app
python3 app.py
