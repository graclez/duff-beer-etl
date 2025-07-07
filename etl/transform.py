
import pandas as pd
from pathlib import Path
import logging

# Configuración de logging
logging.basicConfig(
    filename='etl.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_etl():
    try:
        input_path = Path(__file__).parent.parent / "data" / "orders.csv"
        output_path = Path(__file__).parent.parent / "output" / "orders_summary.csv"

        logging.info(f"Leyendo archivo desde {input_path}")
        df = pd.read_csv(input_path)

        required_columns = {'client_id', 'client_name', 'order_id', 'product_price', 'product_ccf'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise ValueError(f"Faltan columnas requeridas: {missing}")

        df.dropna(subset=['client_id', 'client_name', 'order_id', 'product_price', 'product_ccf'], inplace=True)

        df['total_price'] = df['product_price'] * df['product_ccf']
        df = df[df['total_price'] >= 0]

        summary = df.groupby(['client_id', 'client_name']).agg(
            total_orders=('order_id', 'count'),
            total_sales=('total_price', 'sum')
        ).reset_index()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        summary.to_csv(output_path, index=False)

        logging.info(f"Archivo procesado y guardado en {output_path}")

    except Exception as e:
        logging.error(f"Error en el proceso ETL: {str(e)}", exc_info=True)

if __name__ == "__main__":
    run_etl()
