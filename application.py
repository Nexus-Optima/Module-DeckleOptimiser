from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

application = Flask(__name__)
CORS(application)


@application.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        try:
            df = pd.read_excel(file)
            data = df.to_dict(orient='records')
            return jsonify({'message': 'File processed successfully', 'data': data}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True)
