import pandas as pd
from pathlib import Path
import sys

# Definir rutas
input_path = Path(__file__).parent.parent / "data" / "orders.csv"
output_path = Path(__file__).parent.parent / "output" / "orders_summary.csv"

def main():
    print("🔄 Iniciando proceso ETL...")

    # Verificar que el archivo exista
    if not input_path.exists():
        print(f"❌ ERROR: No se encontró el archivo de entrada en {input_path}")
        sys.exit(1)

    try:
        print("📥 Leyendo archivo CSV...")
        df = pd.read_csv(input_path)
    except Exception as e:
        print(f"❌ ERROR al leer el archivo CSV: {e}")
        sys.exit(1)

    try:
        print("🧠 Procesando datos...")
        df['total_price'] = df['product_price'] * df['product_ccf']

        summary = df.groupby(['client_id', 'client_name']).agg(
            total_orders=('order_id', 'count'),
            total_sales=('total_price', 'sum')
        ).reset_index()
    except Exception as e:
        print(f"❌ ERROR durante la transformación de datos: {e}")
        sys.exit(1)

    try:
        print(f"💾 Guardando archivo procesado en {output_path}")
        summary.to_csv(output_path, index=False)
        print("✅ Proceso ETL finalizado con éxito.")
    except Exception as e:
        print(f"❌ ERROR al guardar el archivo procesado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
