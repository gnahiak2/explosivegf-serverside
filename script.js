let scale;
let config;

function updateImage() {
    if (!config) return; // Wait for config to load
    // Hide all images
    for (let i = 1; i <= config.images.length; i++) {
        document.getElementById('gfImg' + i).style.display = 'none';
    }
    // Find and show the appropriate image based on scale
    for (let i = 0; i < config.images.length; i++) {
        const imgConfig = config.images[i];
        if (scale >= imgConfig.range[0] && scale <= imgConfig.range[1]) {
            document.getElementById('gfImg' + (i + 1)).style.display = 'block';
            break;
        }
    }
}

// Load config and initialize
document.addEventListener('DOMContentLoaded', async function () {
    try {
        const response = await fetch('config.json');
        config = await response.json();
        scale = config.anger;
    } catch (error) {
        console.error('Failed to load config.json:', error);
        return;
    }

    // Update face gesture with anger level
    const faceGesture = document.getElementById('faceGesture');
    faceGesture.textContent = 'Anger: ' + scale;

    // Create images
    const gfSprite = document.getElementById('gfSprite');
    for (let i = 0; i < config.images.length; i++) {
        const img = document.createElement('img');
        img.id = 'gfImg' + i;
        img.src = 'image' + i + '.jpeg';
        img.style.display = 'none';
        gfSprite.appendChild(img);
    }

    // Initial update
    updateImage();
});