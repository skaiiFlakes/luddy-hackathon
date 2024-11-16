from flask import Flask, jsonify, request
from flask_cors import CORS
from prompt import prompt

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'https://g4ntt.vercel.app/'])

@app.route('/api/home', methods=['GET'])
def return_home():
    data = prompt({})
    return jsonify(data)

@app.route('/api/submit', methods=['POST'])
def submit_form():
    if not request.is_json:
        return jsonify({'error': 'Content type must be application/json'}), 400

    data = request.get_json()

    # Validate required fields
    required_fields = ['industry', 'kpi', 'currentStatus', 'targetStatus', 'deadline']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            'error': f'Missing required fields: {", ".join(missing_fields)}'
        }), 400

    try:
        # Process the form data with your prompt function
        result = prompt(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
