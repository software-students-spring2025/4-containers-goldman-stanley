document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const recordButton = document.getElementById('recordButton');
    const timerDisplay = document.getElementById('timer');
    const statusMessage = document.getElementById('statusMessage');
    const resultDisplay = document.getElementById('resultDisplay');
    const silenceBar = document.getElementById('silenceBar');
    const musicBar = document.getElementById('musicBar');
    const speechBar = document.getElementById('speechBar');
    const historyList = document.getElementById('historyList');
    
    // Audio context and recorder
    let audioContext;
    let recorder;
    let audioStream;
    let analyser;
    let isRecording = false;
    let recordingStartTime;
    let timerInterval;
    
    // Initialize visualizer
    const visualizer = new AudioVisualizer('visualizer');
    
    // Event listeners
    recordButton.addEventListener('click', toggleRecording);
    
    // Functions
    async function toggleRecording() {
        if (isRecording) {
            stopRecording();
        } else {
            await startRecording();
        }
    }
    
    async function startRecording() {
        try {
            // Request microphone access
            audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
            
            // Initialize audio context if not already done
            if (!audioContext) {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
            }
            
            // Setup audio analyzer for visualization
            const source = audioContext.createMediaStreamSource(audioStream);
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 2048;
            source.connect(analyser);
            
            // Start the visualizer
            visualizer.connectAnalyser(analyser);
            visualizer.start();
            
            // Initialize recorder
            recorder = new AudioRecorder(audioStream);
            recorder.startRecording();
            
            // Update UI
            recordButton.classList.add('recording');
            recordButton.querySelector('.btn-text').textContent = 'Stop Recording';
            statusMessage.textContent = 'Recording in progress...';
            
            // Start timer
            isRecording = true;
            recordingStartTime = Date.now();
            startTimer();
            
        } catch (error) {
            console.error('Error starting recording:', error);
            statusMessage.textContent = 'Error: ' + (error.message || 'Could not access microphone');
        }
    }
    
    function stopRecording() {
        if (!recorder) return;
        
        // Stop the recorder and get the audio data
        recorder.stopRecording()
            .then(audioBlob => {
                // Update UI
                recordButton.classList.remove('recording');
                recordButton.querySelector('.btn-text').textContent = 'Start Recording';
                statusMessage.textContent = 'Processing audio...';
                
                // Stop timer
                isRecording = false;
                clearInterval(timerInterval);
                
                // Stop visualizer
                visualizer.stop();
                
                // Stop all tracks on the stream
                if (audioStream) {
                    audioStream.getTracks().forEach(track => track.stop());
                }
                
                // Send audio to server for classification
                return sendAudioForClassification(audioBlob);
            })
            .then(result => {
                // Display the results
                displayResults(result);
                // Add to history
                addToHistory(result);
                
                statusMessage.textContent = 'Ready to record';
            })
            .catch(error => {
                console.error('Error in recording process:', error);
                statusMessage.textContent = 'Error: ' + (error.message || 'An error occurred during recording');
            });
    }
    
    function startTimer() {
        timerInterval = setInterval(() => {
            const elapsedMilliseconds = Date.now() - recordingStartTime;
            const elapsedSeconds = Math.floor(elapsedMilliseconds / 1000);
            const minutes = Math.floor(elapsedSeconds / 60);
            const seconds = elapsedSeconds % 60;
            
            timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }, 1000);
    }
    
    async function sendAudioForClassification(audioBlob) {
        // Convert blob to base64
        const reader = new FileReader();
        
        return new Promise((resolve, reject) => {
            reader.onloadend = async function() {
                try {
                    const base64Audio = reader.result;
                    
                    const response = await fetch('/classify_buffer', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ audio_data: base64Audio }),
                    });
                    
                    if (!response.ok) {
                        throw new Error(`Server responded with ${response.status}: ${response.statusText}`);
                    }
                    
                    const result = await response.json();
                    resolve(result);
                } catch (error) {
                    reject(error);
                }
            };
            
            reader.onerror = () => {
                reject(new Error('Error reading audio file'));
            };
            
            reader.readAsDataURL(audioBlob);
        });
    }
    
    function displayResults(result) {
        // Clear previous results
        resultDisplay.innerHTML = '';
        
        // Create result display
        const resultClass = document.createElement('div');
        resultClass.className = `result-class ${result.class}`;
        resultClass.textContent = formatClassName(result.class);
        resultDisplay.appendChild(resultClass);
        
        // Update probability bars
        const silenceProb = result.probabilities.silence * 100;
        const musicProb = result.probabilities.music * 100;
        const speechProb = result.probabilities.speech_noise * 100;
        
        silenceBar.style.width = `${silenceProb}%`;
        silenceBar.textContent = `${silenceProb.toFixed(1)}%`;
        
        musicBar.style.width = `${musicProb}%`;
        musicBar.textContent = `${musicProb.toFixed(1)}%`;
        
        speechBar.style.width = `${speechProb}%`;
        speechBar.textContent = `${speechProb.toFixed(1)}%`;
    }
    
    function addToHistory(result) {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        
        const formattedClassName = formatClassName(result.class);
        const iconClass = result.class === 'speech_noise' ? 'speech-noise-icon' : `${result.class}-icon`;
        
        historyItem.innerHTML = `
            <div class="history-result">
                <div class="history-icon ${iconClass}"></div>
                <div>${formattedClassName}</div>
            </div>
            <div class="history-time">${timeString}</div>
        `;
        
        // Add to the top of the list
        if (historyList.firstChild) {
            historyList.insertBefore(historyItem, historyList.firstChild);
        } else {
            historyList.appendChild(historyItem);
        }
        
        // Limit history list to 10 items
        while (historyList.children.length > 10) {
            historyList.removeChild(historyList.lastChild);
        }
    }
    
    function formatClassName(className) {
        if (className === 'speech_noise') {
            return 'Speech/Noise';
        }
        return className.charAt(0).toUpperCase() + className.slice(1);
    }
});