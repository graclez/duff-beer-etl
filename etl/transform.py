import pandas as pd
from pathlib import Path

# Definir rutas
input_path = Path(__file__).parent.parent / "data" / "orders.csv"
output_path = Path(__file__).parent.parent / "output" / "orders_summary.csv"

# Leer archivo CSV
df = pd.read_csv(input_path)

# Agregar columna de total por pedido
df['total_price'] = df['product_price'] * df['product_ccf']

# Agrupar por cliente
summary = df.groupby(['client_id', 'client_name']).agg(
    total_orders=('order_id', 'count'),
    total_sales=('total_price', 'sum')
).reset_index()

# Guardar archivo procesado
summary.to_csv(output_path, index=False)
