let scale;
let config;
let configPollInterval;

function updateImage() {
    if (!config) return; // Wait for config to load
    // Hide all images
    for (let i = 1; i <= config.images.length; i++) {
        const imgElement = document.getElementById('gfImg' + i);
        if (imgElement) {
            imgElement.style.display = 'none';
        }
    }
    // Find and show the appropriate image based on scale
    for (let i = 0; i < config.images.length; i++) {
        const imgConfig = config.images[i];
        if (scale >= imgConfig.range[0] && scale <= imgConfig.range[1]) {
            const imgElement = document.getElementById('gfImg' + (i + 1));
            if (imgElement) {
                imgElement.style.display = 'block';
            }
            break;
        }
    }
}

async function loadConfig() {
    try {
        const response = await fetch('config.json?t=' + Date.now()); // Add timestamp to prevent caching
        config = await response.json();
        scale = config.anger;
        
        // Update face gesture with anger level
        const faceGesture = document.getElementById('faceGesture');
        if (faceGesture) {
            faceGesture.textContent = 'Anger: ' + scale;
        }
        
        // Update image
        updateImage();
    } catch (error) {
        console.error('Failed to load config.json:', error);
    }
}

// Load config and initialize
document.addEventListener('DOMContentLoaded', async function () {
    // Load initial config
    await loadConfig();

    // Create images
    const gfSprite = document.getElementById('gfSprite');
    if (gfSprite && config) {
        for (let i = 0; i < config.images.length; i++) {
            const img = document.createElement('img');
            img.id = 'gfImg' + (i + 1); // IDs: gfImg1, gfImg2, etc.
            img.src = config.images[i].src;
            img.style.display = 'none';
            gfSprite.appendChild(img);
        }
    }

    // Initial update
    updateImage();
    
    // Poll config.json every 2 seconds to check for updates
    configPollInterval = setInterval(loadConfig, 2000);
});

// Send user message function
async function sendValue() {
    const userInput = document.getElementById('userInput');
    const gfText = document.getElementById('gfText');
    
    if (!userInput) return;
    
    const message = userInput.value.trim();
    if (!message) return;
    
    // Show user message
    if (gfText) {
        gfText.innerHTML = '<p><strong>You:</strong> ' + message + '</p><p>Waiting for response...</p>';
    }
    
    // Clear input
    userInput.value = '';
    
    // Try to send via WebSocket if available
    const websocket = window.ws || (typeof ws !== 'undefined' ? ws : null);
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({ type: 'message', content: message }));
        console.log('Sent via WebSocket:', message);
    } else {
        // Fallback: Try HTTP POST to /chat endpoint
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (response.ok) {
                const data = await response.json();
                if (gfText) {
                    gfText.innerHTML = '<p><strong>You:</strong> ' + message + '</p><p><strong>Girlfriend:</strong> ' + data.response + '</p>';
                }
                // Force reload config to update anger level
                await loadConfig();
            } else {
                throw new Error('HTTP request failed');
            }
        } catch (error) {
            // If both WebSocket and HTTP fail, show error
            console.error('Failed to send message:', error);
            if (gfText) {
                gfText.innerHTML = '<p><strong>You:</strong> ' + message + '</p><p style="color: red;">Error: Could not connect to server. Make sure the backend is running.</p>';
            }
        }
    }
}

// Make sendValue available globally
window.sendValue = sendValue;