let ws;

// Wait for DOM to load before initializing WebSocket
document.addEventListener('DOMContentLoaded', function() {
    // Initialize WebSocket connection
    try {
        ws = new WebSocket('ws://localhost:8765');

        ws.onopen = () => {
            console.log("Connected to websocket port 8765.");
        }

        ws.onmessage = (e) => {
            try {
                const receivedData = JSON.parse(e.data);
                console.log('WebSocket received:', receivedData);
                let userFace = document.getElementById("userFaceGesture");
                userFace.innerText = receivedData.expression;
                // Add any handling you need here
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        }

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        ws.onclose = () => {
            console.log('WebSocket connection closed');
        };
        
        // Make ws available globally
        window.ws = ws;
    } catch (error) {
        console.error('Failed to create WebSocket connection:', error);
    }
});