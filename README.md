# Duff Beer ETL Project (Simulado sin AWS)

Este proyecto simula un pipeline ETL serverless para Duff Beer Inc. sin usar servicios reales de AWS. Utiliza Python para leer, transformar y exponer datos de órdenes.

## Estructura:
- `data/`: contiene el CSV original con los pedidos.
- `etl/`: script para transformar los datos.
- `output/`: resultados transformados.
- `api/`: API simulada con Flask para consultar datos.
- `queries/`: SQLs como si fueran consultas en Athena.
- `models/`: modelado de datos.
- `architecture/`: diagrama del flujo ETL.

## Cómo ejecutar:

1. Instalar dependencias:
```
pip install flask pandas
```

2. Ejecutar ETL:
```
python etl/transform.py
```

3. Iniciar API:
```
python api/app.py
```

4. Consultar API en el navegador:
- `http://localhost:5000/orders/1001`
