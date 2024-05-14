const express = require('express');
const http = require('http');
const path = require('path');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

let frameCount = 1395000;

// Function to generate LTC timecode in HH:MM:SS:FF format
function generateTimecode() {
    const framesPerSecond = 25; // Change this according to your frame rate
    const frames = frameCount % framesPerSecond;
    const seconds = Math.floor(frameCount / framesPerSecond) % 60;
    const minutes = Math.floor(frameCount / (framesPerSecond * 60)) % 60;
    const hours = Math.floor(frameCount / (framesPerSecond * 60 * 60));
    
    // Format timecode with leading zeros
    const timecode = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}:${String(frames).padStart(2, '0')}`;
    
    return timecode;
}

// Start emitting simulated LTC timecode
setInterval(() => {
    const timecode = generateTimecode();
    console.log('Simulated timecode:', timecode);
    io.sockets.emit('timecode', timecode); // Emit timecode to clients
    frameCount++; // Increment frame count
}, 1000 / 25); // Adjust the interval according to your frame rate

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
