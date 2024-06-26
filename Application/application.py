from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from Algorithm.optimiser import optimise_deckle
from Database.s3_operations import get_knives_results, get_wastage_results
from Preprocessing.pre_process import split_dataframe

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
            df.columns = df.columns.str.strip()
            dfs = split_dataframe(df)
            product_types = []
            product_config = []
            for name, df_group in dfs.items():
                if name[0] not in product_types:
                    product_types.append(name[0])
                if str(name[1]) + '_' + str(name[2]) + '_' + str(name[3]) not in product_config:
                    product_config.append(str(name[1]) + '_' + str(name[2]) + '_' + str(name[3]))
                client_metadata = {
                    'client_name': 'CPFL',
                    'order_config': name,
                }
                optimise_deckle(client_metadata, df_group)
            product_metadata = {
                'product_type': product_types,
                'product_config': product_config
            }
            return jsonify({'message': 'File processed successfully', 'data': product_metadata}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@application.route('/api/fetch_plan_data', methods=['GET'])
def get_plan_data():
    algorithm = request.args.get('algorithm')
    client_name = request.args.get('client_name')
    product_name = request.args.get('product_name')
    product_config = request.args.get('product_config')
    if algorithm not in ['knives', 'wastage']:
        return jsonify({'error': 'Invalid algorithm name'}), 400
    if algorithm == 'knives':
        result = get_knives_results(client_name, product_name, product_config)
    else:
        result = get_wastage_results(client_name, product_name, product_config)
    return result


if __name__ == '__main__':
    application.run(host="0.0.0.0", debug=True)
