// -------------------
// Global variables
// -------------------
let scale = 75; // Initial anger level (0 = angry, 100 = calm)
const appConfig = window.APP_CONFIG || {};
const defaultApiBase = (window.location.origin && window.location.origin !== 'null')
    ? window.location.origin
    : 'http://localhost:8888';
const apiBase = appConfig.apiBase || defaultApiBase;

// -------------------
// Update scale and image
// -------------------
function updateScale(value) {
    scale = parseInt(value);
    updateImage();
}

function updateImage() {
    // Hide all images
    for (let i = 1; i <= 5; i++) {
        const img = document.getElementById('gfImg' + i);
        if (img) img.style.display = 'none';
    }

    // Determine which image to show based on scale
    let imageIndex;
    if (scale < 20) imageIndex = 1;
    else if (scale < 40) imageIndex = 2;
    else if (scale < 60) imageIndex = 3;
    else if (scale < 80) imageIndex = 4;
    else imageIndex = 5;

    const img = document.getElementById('gfImg' + imageIndex);
    if (img) img.style.display = 'block';
}

// -------------------
// Update face gesture
// -------------------
function updateFaceGesture(angerLevel) {
    const faceGesture = document.getElementById('faceGesture');
    const angerLvlDiv = document.getElementById('angerLvl');
    if (!faceGesture) return;

    if (angerLevel >= 80) faceGesture.textContent = 'Explosive 💥';
    else if (angerLevel >= 60) faceGesture.textContent = 'Very Angry 😡';
    else if (angerLevel >= 40) faceGesture.textContent = 'Angry 😠';
    else if (angerLevel >= 20) faceGesture.textContent = 'Upset 😐';
    else faceGesture.textContent = 'Calm 😊';

    if (angerLvlDiv) {
        angerLvlDiv.textContent = `Anger Level: ${angerLevel}`;
    }
}

// -------------------
// Send user message to backend
// -------------------
async function sendValue() {
    const userInput = document.getElementById('userInput');
    const gfText = document.getElementById('gfText');
    const gfSprite = document.getElementById('gfSprite');
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

    // ----------------
    // Show loading sprite
    // ----------------
    if (gfSprite) {
        // Hide all regular images
        for (let i = 1; i <= 5; i++) {
            const img = document.getElementById('gfImg' + i);
            if (img) img.style.display = 'none';
        }

        // Check if loading image exists
        let loadingImg = document.getElementById('gfLoading');
        if (!loadingImg) {
            loadingImg = document.createElement('img');
            loadingImg.id = 'gfLoading';
            loadingImg.src = 'gfLoading.gif';
            loadingImg.style.width = '300px';
            loadingImg.style.height = 'auto';
            gfSprite.appendChild(loadingImg);
        }
        loadingImg.style.display = 'block';
    }

    gfText.innerHTML = '<p>Thinking...</p>';

    try {
        const response = await fetch(new URL('/api/chat', apiBase), {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (data.success) {
            gfText.innerHTML = `<p>${data.response}</p>`;

            // Update scale and face gesture
            const invertedScale = 100 - data.anger_level;
            updateScale(invertedScale);
            updateFaceGesture(data.anger_level);

            userInput.value = '';
        } else {
            gfText.innerHTML = `<p style="color: red;">Error: ${data.error || 'Unknown error'}</p>`;
        }
    } catch (err) {
        console.error(err);
        gfText.innerHTML = `<p style="color: red;">Failed to connect to server. Make sure it is running on ${apiBase}</p>`;
    } finally {
        // ----------------
        // Hide loading and show normal sprite
        // ----------------
        if (gfSprite) {
            const loadingImg = document.getElementById('gfLoading');
            if (loadingImg) loadingImg.style.display = 'none';
            updateImage(); // Show the correct image based on current scale
        }

        userInput.disabled = false;
        sendButton.disabled = false;
        sendButton.textContent = originalButtonText;
        userInput.focus();
    }
}


// -------------------
// Initialize DOM elements
// -------------------
document.addEventListener('DOMContentLoaded', function() {
    const gfSprite = document.getElementById('gfSprite');
    if (gfSprite) {
        for (let i = 1; i <= 5; i++) {
            const img = document.createElement('img');
            img.id = 'gfImg' + i;
            img.src = `image${i}.gif`;
            img.style.display = 'none';
            img.style.width = '300px';
            img.style.height = 'auto';

            // Placeholder if image fails
            img.onerror = function() {
                const placeholder = document.createElement('div');
                placeholder.id = this.id;
                placeholder.style.width = '300px';
                placeholder.style.height = '300px';
                placeholder.style.display = 'flex';
                placeholder.style.alignItems = 'center';
                placeholder.style.justifyContent = 'center';
                placeholder.style.background = ['#ff6b6b', '#ffd93d', '#6bcf7f', '#4d96ff', '#b794f6'][i-1];
                placeholder.style.color = 'white';
                placeholder.style.fontSize = '48px';
                placeholder.style.fontWeight = 'bold';
                placeholder.textContent = ['💥', '😡', '😠', '😐', '😊'][i-1];
                this.parentNode.replaceChild(placeholder, this);
            };

            gfSprite.appendChild(img);
        }
    }

    // Show initial face gesture
    updateFaceGesture(scale);
    updateImage();

    // Send button
    const sendButton = document.getElementById('sendButton');
    if (sendButton) {
        sendButton.addEventListener('click', function(e) {
            e.preventDefault();
            sendValue();
        });
    }

    // Enter key triggers send
    const userInput = document.getElementById('userInput');
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendValue();
            }
        });
    }
});
