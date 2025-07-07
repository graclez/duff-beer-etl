from flask import Flask, jsonify
import pandas as pd
from pathlib import Path

app = Flask(__name__)
data_path = Path(__file__).parent.parent / "output" / "orders_summary.csv"
data = pd.read_csv(data_path)

@app.route('/orders/<int:client_id>', methods=['GET'])
def get_orders_by_client(client_id):
    result = data[data['client_id'] == client_id]
    return jsonify(result.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
