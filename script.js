let scale;
let config;
let configPollInterval;

function updateScale(value) {
    scale = parseInt(value);
    updateImage();
}

function updateImage() {
    // If config exists, use config-based logic
    if (config && config.images) {
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
    } else {
        // Fallback: simple logic for gfLVL1-5 images
        for (let i = 1; i <= 5; i++) {
            const imgElement = document.getElementById('gfImg' + i);
            if (imgElement) {
                imgElement.style.display = 'none';
            }
        }
        // Show the appropriate image based on scale (0-100 maps to 1-5)
        let index = Math.floor(scale / 25) + 1;
        if (index > 5) index = 5;
        if (index < 1) index = 1;
        const imgElement = document.getElementById('gfImg' + index);
        if (imgElement) {
            imgElement.style.display = 'block';
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
            img.id = 'gfImg' + (i + 1); // Fix: use i+1 to match the updateImage function
            img.src = 'image' + (i + 1) + '.gif';
            img.style.display = 'none';
            gfSprite.appendChild(img);
        }
    }

    // Initial update
    updateImage();
    
    // Set initial anger level display (75 = Slightly Upset)
    updateFaceGesture(75);
});

// Send message to AI and update UI
async function sendValue() {
    const userInput = document.getElementById('userInput');
    const gfText = document.getElementById('gfText');
    const message = userInput.value.trim();
    
    // Check if message is empty
    if (!message) {
        alert('Please enter a message!');
        return;
    }
    
    // Disable input and button while processing
    userInput.disabled = true;
    const sendButton = document.querySelector('button[onclick="sendValue()"]');
    const originalButtonText = sendButton.textContent;
    sendButton.disabled = true;
    sendButton.textContent = 'Sending...';
    
    // Show loading state
    gfText.innerHTML = '<p>Thinking...</p>';
    
    try {
        // Send POST request to Flask API
        const response = await fetch('http://localhost:8888/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            // Update AI response text
            gfText.innerHTML = `<p>${data.response}</p>`;
            
            // Update image based on anger level (0-100 maps to 0-100 scale)
            // Higher anger = lower scale (more angry = angrier image)
            // 100 anger = 0 scale (most angry = gfLVL1), 0 anger = 100 scale (calm = gfLVL5)
            const invertedScale = 100 - data.anger_level;
            updateScale(invertedScale);
            
            // Update face gesture based on anger level
            updateFaceGesture(data.anger_level);
            
            // Clear input field
            userInput.value = '';
        } else {
            // Handle error response
            gfText.innerHTML = `<p style="color: red;">Error: ${data.error || 'Unknown error'}</p>`;
        }
    } catch (error) {
        console.error('Error:', error);
        gfText.innerHTML = `<p style="color: red;">Failed to connect to server. Make sure the Flask server is running on http://localhost:8888</p>`;
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = originalButtonText;
        userInput.focus();
    }
}

// Update face gesture based on anger level (higher = more angry)
function updateFaceGesture(angerLevel) {
    const faceGesture = document.getElementById('faceGesture');
    
    if (angerLevel >= 80) {
        faceGesture.textContent = 'Explosive/Cold War 💢';
    } else if (angerLevel >= 60) {
        faceGesture.textContent = 'Very Angry 😡';
    } else if (angerLevel >= 40) {
        faceGesture.textContent = 'Obviously Angry 😠';
    } else if (angerLevel >= 20) {
        faceGesture.textContent = 'Slightly Upset 😐';
    } else {
        faceGesture.textContent = 'Calm/Happy 😊';
    }
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', function() {
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendValue();
            }
        });
    }
});
