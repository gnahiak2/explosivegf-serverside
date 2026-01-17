let scale = 75; // Initial anger level

function updateScale(value) {
    scale = parseInt(value);
    console.log('updateScale called with:', value, 'scale is now:', scale);
    updateImage();
}

function updateImage() {
    console.log('updateImage called, scale:', scale);
    
    // Hide all images
    for (let i = 1; i <= 5; i++) {
        const imgElement = document.getElementById('gfImg' + i);
        if (imgElement) {
            imgElement.style.display = 'none';
        }
    }
    
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
    }
}

// Load config and initialize
document.addEventListener('DOMContentLoaded', async function () {
    console.log('DOM loaded');

    // Create images (or placeholders)
    const gfSprite = document.getElementById('gfSprite');
    if (gfSprite) {
        console.log('Creating image elements');
        for (let i = 1; i <= 5; i++) {
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
    
    // Set initial anger level display
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
    
    gfText.innerHTML = '<p>Thinking...</p>';
    
    try {
        // Get user's facial expression from the userFaceGesture div
        const userFaceGesture = document.getElementById('userFaceGesture');
        const userExpression = userFaceGesture ? userFaceGesture.textContent : 'neutral';
        
        const response = await fetch('http://localhost:8888/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                user_expression: userExpression  // Send the expression too
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Received from API:', data);
        
        if (data.success) {
            gfText.innerHTML = `<p>${data.response}</p>`;
            updateScale(data.anger_level);
            updateFaceGesture(data.anger_level);
            userInput.value = '';
        } else {
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
    const angerLvl = document.getElementById('angerLvl');
    if (angerLvl) {
        angerLvl.textContent = angerLevel;
    }

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
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            sendValue();
        });
    }
    
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                e.stopPropagation();
                sendValue();
            }
        });
    }
});