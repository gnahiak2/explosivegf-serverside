"""
Flask server for Explosive Girlfriend AI
Provides REST API endpoint for chat functionality
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from girlfriend_ai import ExplosiveGirlfriendAI
import time
import threading

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Initialize AI instance (singleton memory)
ai = ExplosiveGirlfriendAI()

# -----------------------------
# HEARTBEAT / DISCONNECT LOGIC
# -----------------------------
last_ping = time.time()
PING_TIMEOUT = 10  # seconds

@app.route('/api/ping', methods=['POST'])
def ping():
    global last_ping
    last_ping = time.time()
    return jsonify({"ok": True}), 200


def watchdog():
    global last_ping, ai
    while True:
        time.sleep(2)
        if time.time() - last_ping > PING_TIMEOUT:
            print("💀 Client disconnected — resetting AI memory")
            ai.reset_conversation()
            last_ping = time.time()  # prevent infinite reset spam


# Start watchdog thread
threading.Thread(target=watchdog, daemon=True).start()

# -----------------------------
# ROUTES
# -----------------------------

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing message field'
            }), 400

        user_input = data['message'].strip()

        if not user_input:
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400

        result = ai.chat(user_input)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'anger_level': ai.conversation.get_last_anger_level(),
            'response': 'Hmph... something went wrong on the server side.'
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    try:
        status = ai.get_emotion_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    try:
        ai.reset_conversation()
        return jsonify({
            'success': True,
            'reset': True,
            'message': 'Conversation reset'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'reset': False,
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Explosive Girlfriend AI API'
    }), 200


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8888,
        debug=False
    )
