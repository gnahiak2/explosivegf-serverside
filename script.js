let scale = 75;

function updateScale(value) {
    scale = parseInt(value);
    document.getElementById('scaleValue').textContent = scale;
    updateImage();
}

function updateImage() {
    // Hide all images
    for (let i = 1; i <= 5; i++) {
        document.getElementById('gfImg' + i).style.display = 'none';
    }
    // Show the appropriate image based on scale
    let index = Math.floor(scale / 20) + 1;
    if (index > 5) index = 5;
    document.getElementById('gfImg' + index).style.display = 'block';
}

// Create the slider and images dynamically
document.addEventListener('DOMContentLoaded', function() {
    // Create slider label
    const label = document.createElement('label');
    label.setAttribute('for', 'scaleInput');
    label.textContent = 'Scale: ';
    
    // Create slider input
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.id = 'scaleInput';
    slider.min = '0';
    slider.max = '100';
    slider.value = '50';
    slider.addEventListener('input', function() {
        updateScale(this.value);
    });
    
    // Create value span
    const valueSpan = document.createElement('span');
    valueSpan.id = 'scaleValue';
    valueSpan.textContent = '50';
    
    // Append to body after h1
    const h1 = document.querySelector('h1');
    h1.insertAdjacentElement('afterend', label);
    label.insertAdjacentElement('afterend', slider);
    slider.insertAdjacentElement('afterend', valueSpan);
    
    // Create images
    const gfSprite = document.getElementById('gfSprite');
    for (let i = 1; i <= 5; i++) {
        const img = document.createElement('img');
        img.id = 'gfImg' + i;
        img.src = 'image' + i + '.jpg';
        img.style.display = 'none';
        gfSprite.appendChild(img);
    }
    
    // Initial update
    updateImage();
});