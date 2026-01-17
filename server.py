"""
Flask server for Explosive Girlfriend AI
Provides REST API endpoint for chat functionality
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from girlfriend_ai import ExplosiveGirlfriendAI

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Initialize AI instance (singleton to maintain conversation history)
ai = ExplosiveGirlfriendAI()

@app.route('/')
def index():
    """
    Serve the main HTML page
    """
    return app.send_static_file('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat API endpoint
    Receives user message and returns AI response
    """
    try:
        # Get JSON data from request
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
        
        # Get AI response
        result = ai.chat(user_input)
        
        # Return response
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
    """
    Get current emotion status
    """
    try:
        status = ai.get_emotion_status()
        return jsonify(status), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """
    Reset conversation history
    """
    try:
        ai.reset_conversation()
        return jsonify({
            'success': True,
            'message': 'Conversation reset'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Explosive Girlfriend AI API'
    }), 200

if __name__ == '__main__':
    PORT = 8888
    print("Starting Explosive Girlfriend AI Server...")
    print(f"Frontend: http://localhost:{PORT}/")
    print(f"API endpoint: http://localhost:{PORT}/api/chat")
    print(f"Health check: http://localhost:{PORT}/health")
    app.run(debug=True, port=PORT)

