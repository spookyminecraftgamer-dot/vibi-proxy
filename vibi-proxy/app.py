import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    ngrok_url = os.environ.get('NGROK_URL', '')
    if not ngrok_url:
        return jsonify({'response': 'Vibi AI is offline. Start the Kaggle notebook first!'}), 503
    try:
        response = requests.post(
            f'{ngrok_url}/chat',
            json=request.json,
            headers={'ngrok-skip-browser-warning': 'true'},
            timeout=120
        )
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'response': 'Vibi AI is offline. Start the Kaggle notebook first!'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))