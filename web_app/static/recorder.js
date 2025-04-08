/**
 * AudioRecorder class for recording audio using the MediaRecorder API
 */
class AudioRecorder {
    constructor(stream) {
        this.stream = stream;
        this.chunks = [];
        
        // Configure the MediaRecorder
        const options = { mimeType: 'audio/webm' };
        try {
            this.mediaRecorder = new MediaRecorder(stream, options);
        } catch (e) {
            // Fallback if the preferred mimeType is not supported
            console.warn(`MediaRecorder could not be created with mimeType ${options.mimeType}. Using default mimeType.`);
            this.mediaRecorder = new MediaRecorder(stream);
        }
        
        // Event handlers
        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.chunks.push(event.data);
            }
        };
    }
    
    /**
     * Start recording audio
     */
    startRecording() {
        this.chunks = [];
        this.mediaRecorder.start();
    }
    
    /**
     * Stop recording and return the recorded audio as a Blob
     * @returns {Promise} Promise that resolves with the audio Blob
     */
    stopRecording() {
        return new Promise((resolve) => {
            this.mediaRecorder.onstop = () => {
                // Create a blob from the recorded chunks
                const audioBlob = new Blob(this.chunks, { type: 'audio/wav' });
                resolve(audioBlob);
            };
            
            this.mediaRecorder.stop();
        });
    }
    
    /**
     * Check if currently recording
     * @returns {boolean} True if recording, false otherwise
     */
    isRecording() {
        return this.mediaRecorder && this.mediaRecorder.state === 'recording';
    }
    
    /**
     * Release resources
     */
    dispose() {
        if (this.mediaRecorder) {
            if (this.isRecording()) {
                this.mediaRecorder.stop();
            }
            this.mediaRecorder = null;
        }
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        this.chunks = [];
    }
}