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

@app.route('/start', methods=['POST'])
def start():
    username = os.environ.get('KAGGLE_USERNAME', '')
    api_token = os.environ.get('KAGGLE_API_TOKEN', '')
    kernel_slug = os.environ.get('KAGGLE_KERNEL_SLUG', '')
    
    if not all([username, api_token, kernel_slug]):
        return jsonify({'status': 'error', 'message': 'Kaggle credentials missing'}), 500
    
    try:
        response = requests.post(
            f'https://www.kaggle.com/api/v1/kernels/{username}/{kernel_slug}/run',
            auth=(username, api_token),
            json={}
        )
        if response.status_code in [200, 201]:
            return jsonify({'status': 'ok', 'message': 'Kaggle notebook starting!'})
        else:
            return jsonify({'status': 'error', 'message': response.text}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
