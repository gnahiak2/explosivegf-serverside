<<<<<<< ours
let scale = 75; // Initial anger level

function updateScale(value) {
    scale = parseInt(value);
    console.log('updateScale called with:', value, 'scale is now:', scale);
=======
let scale;
let config;
let configPollInterval;

function updateScale(value) {
    scale = parseInt(value);
>>>>>>> theirs
    updateImage();
}

function updateImage() {
<<<<<<< ours
    console.log('updateImage called, scale:', scale);
    
    // Hide all images
    for (let i = 1; i <= 5; i++) {
        const imgElement = document.getElementById('gfImg' + i);
=======
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
>>>>>>> theirs
        if (imgElement) {
            imgElement.style.display = 'none';
        }
    }
<<<<<<< ours
    
    // Determine which image to show based on scale (0-120)
    let imageIndex;
    if (scale < 20) {
        imageIndex = 1; // 0-19: Most angry/explosive
    } else if (scale < 40) {
        imageIndex = 2; // 20-39: Very angry
    } else if (scale < 60) {
        imageIndex = 3; // 40-59: Obviously angry
    } else if (scale < 80) {
        imageIndex = 4; // 60-79: Slightly upset
    } else {
        imageIndex = 5; // 80-120: Calm/happy
    }
    
    console.log('Showing image index:', imageIndex);
    
    const imgElement = document.getElementById('gfImg' + imageIndex);
    if (imgElement) {
        imgElement.style.display = 'block';
        console.log('Displayed:', imgElement.id);
    } else {
        console.error('Image element not found:', 'gfImg' + imageIndex);
=======
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
>>>>>>> theirs
    }
}

// Load config and initialize
document.addEventListener('DOMContentLoaded', async function () {
    console.log('DOM loaded');

    // Create images (or placeholders)
    const gfSprite = document.getElementById('gfSprite');
<<<<<<< ours
    if (gfSprite) {
        console.log('Creating image elements');
        for (let i = 1; i <= 5; i++) {
=======
    if (gfSprite && config) {
        for (let i = 0; i < config.images.length; i++) {
>>>>>>> theirs
            const img = document.createElement('img');
            img.id = 'gfImg' + i;
            img.src = 'image' + i + '.gif';
            img.style.display = 'none';
            img.style.width = '300px';
            img.style.height = 'auto';
            
            // If image fails to load, show colored placeholder
            img.onerror = function() {
                console.warn('Image not found:', this.src, '- using placeholder');
                const placeholder = document.createElement('div');
                placeholder.id = this.id;
                placeholder.style.width = '300px';
                placeholder.style.height = '300px';
                placeholder.style.display = this.style.display;
                placeholder.style.background = ['#ff6b6b', '#ffd93d', '#6bcf7f', '#4d96ff', '#b794f6'][i-1];
                placeholder.style.border = '3px solid #333';
                placeholder.style.fontSize = '48px';
                placeholder.style.fontWeight = 'bold';
                placeholder.style.display = 'flex';
                placeholder.style.alignItems = 'center';
                placeholder.style.justifyContent = 'center';
                placeholder.style.color = 'white';
                placeholder.style.textShadow = '2px 2px 4px rgba(0,0,0,0.5)';
                placeholder.textContent = ['💥', '😡', '😠', '😐', '😊'][i-1];
                this.parentNode.replaceChild(placeholder, this);
            };
            
            gfSprite.appendChild(img);
            console.log('Created image:', img.id, img.src);
        }
    }

    // Initial update
    updateImage();
    
<<<<<<< ours
    // Set initial anger level display
=======
    // Set initial anger level display (75 = Slightly Upset)
>>>>>>> theirs
    updateFaceGesture(75);
});

// Send message to AI and update UI
async function sendValue() {
    const userInput = document.getElementById('userInput');
    const gfText = document.getElementById('gfText');
    const message = userInput.value.trim();
    
    if (!message) {
        alert('Please enter a message!');
        return;
    }
    
    userInput.disabled = true;
    const sendButton = document.getElementById('sendButton');
    const originalButtonText = sendButton.textContent;
    sendButton.disabled = true;
    sendButton.textContent = 'Sending...';
    
<<<<<<< HEAD
<<<<<<< HEAD
    // Try to send via WebSocket if available
    const websocket = window.ws || (typeof ws !== 'undefined' ? ws : null);
    if (websocket && websocket.readyState === WebSocket.OPEN) {
        websocket.send(JSON.stringify({ type: 'message', content: message }));
        console.log('Sent via WebSocket:', message);
=======
=======
>>>>>>> parent of b08e885 (hi)
<<<<<<< ours
=======
    // Show loading state
>>>>>>> theirs
    gfText.innerHTML = '<p>Thinking...</p>';
    
    try {
<<<<<<< HEAD
=======
        // Get user's facial expression from the userFaceGesture div
        const userFaceGesture = document.getElementById('userFaceGesture');
        const userExpression = userFaceGesture ? userFaceGesture.textContent : 'neutral';
        
>>>>>>> parent of b08e885 (hi)
        const response = await fetch('http://localhost:8888/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
<<<<<<< HEAD
            body: JSON.stringify({ message: message })
=======
            body: JSON.stringify({ 
                message: message,
                user_expression: userExpression  // Send the expression too
            })
>>>>>>> parent of b08e885 (hi)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
<<<<<<< HEAD
        }
        
        const data = await response.json();
        console.log('Received from API:', data);
        
        if (data.success) {
<<<<<<< ours
            gfText.innerHTML = `<p>${data.response}</p>`;
            updateScale(data.anger_level);
=======
            // Update AI response text
            gfText.innerHTML = `<p>${data.response}</p>`;
            
            // Update image based on anger level (0-100 maps to 0-100 scale)
            // Higher anger = lower scale (more angry = angrier image)
            // 100 anger = 0 scale (most angry = gfLVL1), 0 anger = 100 scale (calm = gfLVL5)
            const invertedScale = 100 - data.anger_level;
            updateScale(invertedScale);
            
            // Update face gesture based on anger level
>>>>>>> theirs
            updateFaceGesture(data.anger_level);
            userInput.value = '';
        } else {
<<<<<<< ours
=======
            // Handle error response
>>>>>>> theirs
            gfText.innerHTML = `<p style="color: red;">Error: ${data.error || 'Unknown error'}</p>`;
        }
    } catch (error) {
        console.error('Error:', error);
        gfText.innerHTML = `<p style="color: red;">Failed to connect to server. Make sure the Flask server is running on http://localhost:8888</p>`;
    } finally {
        userInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = originalButtonText;
        userInput.focus();
    }
}

// Update face gesture based on anger level (higher = more angry)
function updateFaceGesture(angerLevel) {
<<<<<<< ours
    const angerLvl = document.getElementById('angerLvl');
    if (angerLvl) {
        angerLvl.textContent = angerLevel;
    }

=======
>>>>>>> theirs
    const faceGesture = document.getElementById('faceGesture');
    
    if (angerLevel >= 100) {
        faceGesture.textContent = 'KABOOM 💥';
    } else if (angerLevel >= 80) {
        faceGesture.textContent = 'Explosive/Cold War 💢';
    } else if (angerLevel >= 60) {
        faceGesture.textContent = 'Very Angry 😡';
    } else if (angerLevel >= 40) {
        faceGesture.textContent = 'Obviously Angry 😠';
    } else if (angerLevel >= 20) {
        faceGesture.textContent = 'Slightly Upset 😐';
>>>>>>> parent of ca2f3d3 (Merge branch 'main' of https://github.com/senkyte/explosivegf)
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
=======
>>>>>>> parent of b08e885 (hi)
        }
        
        const data = await response.json();
        console.log('Received from API:', data);
        
        if (data.success) {
<<<<<<< ours
            gfText.innerHTML = `<p>${data.response}</p>`;
            updateScale(data.anger_level);
=======
            // Update AI response text
            gfText.innerHTML = `<p>${data.response}</p>`;
            
            // Update image based on anger level (0-100 maps to 0-100 scale)
            // Higher anger = lower scale (more angry = angrier image)
            // 100 anger = 0 scale (most angry = gfLVL1), 0 anger = 100 scale (calm = gfLVL5)
            const invertedScale = 100 - data.anger_level;
            updateScale(invertedScale);
            
            // Update face gesture based on anger level
>>>>>>> theirs
            updateFaceGesture(data.anger_level);
            userInput.value = '';
        } else {
<<<<<<< ours
=======
            // Handle error response
>>>>>>> theirs
            gfText.innerHTML = `<p style="color: red;">Error: ${data.error || 'Unknown error'}</p>`;
        }
    } catch (error) {
        console.error('Error:', error);
        gfText.innerHTML = `<p style="color: red;">Failed to connect to server. Make sure the Flask server is running on http://localhost:8888</p>`;
    } finally {
        userInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = originalButtonText;
        userInput.focus();
    }
}

// Update face gesture based on anger level (higher = more angry)
function updateFaceGesture(angerLevel) {
<<<<<<< ours
    const angerLvl = document.getElementById('angerLvl');
    if (angerLvl) {
        angerLvl.textContent = angerLevel;
    }

=======
>>>>>>> theirs
    const faceGesture = document.getElementById('faceGesture');
    
    if (angerLevel >= 100) {
        faceGesture.textContent = 'KABOOM 💥';
    } else if (angerLevel >= 80) {
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
<<<<<<< ours
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            sendValue();
        });
    }
    
=======
>>>>>>> theirs
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
<<<<<<< ours
                e.preventDefault();
                e.stopPropagation();
=======
>>>>>>> theirs
                sendValue();
            }
        });
    }
<<<<<<< ours
});
=======
});
>>>>>>> theirs
