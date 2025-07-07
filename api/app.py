from flask import Flask, jsonify
import pandas as pd
from pathlib import Path
import sys

app = Flask(__name__)
data_path = Path(__file__).parent.parent / "output" / "orders_summary.csv"

try:
    print(f"📥 Cargando archivo procesado desde: {data_path}")
    if not data_path.exists():
        raise FileNotFoundError(f"No se encontró el archivo en {data_path}")
    data = pd.read_csv(data_path)
    print(" Archivo cargado exitosamente.")
except Exception as e:
    print(f" ERROR al cargar el archivo: {e}")
    sys.exit(1)

@app.route('/orders/<int:client_id>', methods=['GET'])
def get_orders_by_client(client_id):
    print(f"Buscando pedidos del cliente ID: {client_id}")
    result = data[data['client_id'] == client_id]

    if result.empty:
        print(f" Cliente {client_id} no encontrado.")
        return jsonify({"error": "Cliente no encontrado"}), 404

    return jsonify(result.to_dict(orient='records')), 200

if __name__ == '__main__':
    print("Iniciando API en modo desarrollo...")
    app.run(debug=True)
