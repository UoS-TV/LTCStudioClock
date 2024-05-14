const express = require('express');
const http = require('http');
const path = require('path');
const { exec } = require('child_process');
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

let lastTimecodeReceived = Date.now();

// Start the arecord process to continuously read LTC timecode
const arecordProcess = exec('arecord -D hw:3,0 -f dat -r 48000 -c 2 | stdbuf -o0 ltcdump -');
arecordProcess.stdout.on('data', data => {
    const lines = data.toString().split('\n');
    lines.forEach(line => {
        if (!line.startsWith('#') && !line.includes('User bits')) {
            const match = line.match(/\d{2}:\d{2}:\d{2}:\d{2}/); // Match timecode pattern
            if (match) {
                const timecode = match[0]; // Extract matched timecode
                console.log('Extracted timecode:', timecode);
                io.sockets.emit('timecode', timecode); // Emit timecode to clients
                lastTimecodeReceived = Date.now(); // Update last timecode received timestamp
            }
        }
    });
});

arecordProcess.stderr.on('data', data => {
    const errorMessage = data.toString();
    if (errorMessage.includes('Error')) { // Check if the message contains the word "Error"
        console.error('Error reading LTC timecode:', errorMessage);
        process.exit(1); // Exit the process in case of error
    } else {
        console.log(errorMessage); // Log non-error messages
    }
});

arecordProcess.on('error', error => {
    console.error('arecord process error:', error);
    process.exit(1); // Exit the process in case of error
});

// Restart server if no timecode received after 15 seconds
const restartThreshold = 15 * 1000; // 15 seconds in milliseconds
setInterval(() => {
    if (Date.now() - lastTimecodeReceived > restartThreshold) {
        console.log('No timecode received. Restarting server...');
        process.exit(1);
    }
}, restartThreshold);

// Start the server
const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
