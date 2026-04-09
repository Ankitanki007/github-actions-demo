from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from GitHub Actions Demo!',
        'version': os.environ.get('APP_VERSION', '1.0.0'),
        'status': 'running'
    })


@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200


@app.route('/add')
def add():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify({'result': a + b})


@app.route('/divide')
def divide():
    a = request.args.get('a', 0, type=float)
    b = request.args.get('b', 1, type=float)
    if b == 0:
        return jsonify({'error': 'division by zero'}), 400
    return jsonify({'result': a / b})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
