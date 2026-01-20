from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact form
@app.route('/contact', methods=['POST'])
def contact():
    data = request.json
    # Here you can save to database or send email
    return jsonify({'status': 'Message received!', 'data': data})

# API endpoint
@app.route('/api/hello')
def api_hello():
    name = request.args.get('name', 'World')
    return jsonify({'message': f'Hello, {name}!'})

if __name__ == '__main__':
    # For production: gunicorn app:app
    # For development: python app.py
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
