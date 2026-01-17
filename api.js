const ws = new WebSocket('ws://localhost:8765');

ws.onopen = () => {
    console.log("Connect to websocket port 8765.");
}

let faceGesture = document.getElementById("faceGesture");
ws.onmessage = (e) => {
    recievedData = JSON.parse(e.data)
    faceGesture.innerText = recievedData.expression;
    
}

ws.onerror = (error) => {
  console.error('Error:', error);
};

ws.onclose = () => {
  console.log('Connection closed');
};