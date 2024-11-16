from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000', 'https://g4ntt.vercel.app/'])

@app.route('/api/home', methods=['GET'])
def return_home():
    return jsonify({"message": "Hello, World!", 'people': ['Jack', 'Jill', 'John']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
