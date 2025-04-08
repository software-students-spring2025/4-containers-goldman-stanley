/**
 * AudioVisualizer class for creating real-time audio visualizations
 */
class AudioVisualizer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.canvasCtx = this.canvas.getContext('2d');
        this.analyser = null;
        this.dataArray = null;
        this.animationId = null;
        this.isActive = false;
        
        // Set canvas size to match its display size
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
    }
    
    /**
     * Connect an analyser node to the visualizer
     * @param {AnalyserNode} analyser - Web Audio API analyser node
     */
    connectAnalyser(analyser) {
        this.analyser = analyser;
        this.dataArray = new Uint8Array(this.analyser.frequencyBinCount);
    }
    
    /**
     * Start the visualization
     */
    start() {
        if (!this.analyser) {
            console.warn('Analyser not connected. Call connectAnalyser() first.');
            return;
        }
        
        this.isActive = true;
        this.draw();
    }
    
    /**
     * Stop the visualization
     */
    stop() {
        this.isActive = false;
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        
        // Clear the canvas
        this.clearCanvas();
    }
    
    /**
     * Draw method for rendering the visualization
     */
    draw() {
        if (!this.isActive) return;
        
        this.animationId = requestAnimationFrame(() => this.draw());
        
        // Get the current frequency data
        this.analyser.getByteFrequencyData(this.dataArray);
        
        this.clearCanvas();
        
        // Draw the waveform
        const width = this.canvas.width;
        const height = this.canvas.height;
        const barWidth = width / this.dataArray.length * 2.5;
        let x = 0;
        
        this.canvasCtx.beginPath();
        this.canvasCtx.moveTo(0, height);
        
        for (let i = 0; i < this.dataArray.length; i++) {
            const barHeight = this.dataArray[i] / 255 * height;
            
            // Calculate color based on frequency (from blue to red)
            const hue = i / this.dataArray.length * 220;
            this.canvasCtx.fillStyle = `hsla(${hue}, 100%, 50%, 0.8)`;
            
            // Draw bar
            this.canvasCtx.fillRect(x, height - barHeight, barWidth, barHeight);
            
            x += barWidth + 1;
            if (x > width) break;
        }
    }
    
    /**
     * Clear the canvas
     */
    clearCanvas() {
        const width = this.canvas.width;
        const height = this.canvas.height;
        
        // Clear the canvas
        this.canvasCtx.clearRect(0, 0, width, height);
        
        // Draw background gradient
        const gradient = this.canvasCtx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, 'rgba(240, 246, 255, 0.2)');
        gradient.addColorStop(1, 'rgba(240, 246, 255, 0.8)');
        this.canvasCtx.fillStyle = gradient;
        this.canvasCtx.fillRect(0, 0, width, height);
        
        // Draw grid lines
        this.canvasCtx.strokeStyle = 'rgba(200, 210, 220, 0.5)';
        this.canvasCtx.lineWidth = 1;
        
        // Horizontal grid lines
        const step = height / 8;
        for (let i = 1; i < 8; i++) {
            const y = step * i;
            this.canvasCtx.beginPath();
            this.canvasCtx.moveTo(0, y);
            this.canvasCtx.lineTo(width, y);
            this.canvasCtx.stroke();
        }
    }
    
    /**
     * Resize the canvas to match its display size
     */
    resizeCanvas() {
        const displayWidth = this.canvas.clientWidth;
        const displayHeight = this.canvas.clientHeight;
        
        if (this.canvas.width !== displayWidth || this.canvas.height !== displayHeight) {
            this.canvas.width = displayWidth;
            this.canvas.height = displayHeight;
            
            if (this.isActive) {
                this.clearCanvas();
            }
        }
    }
}