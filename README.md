
# Duff Beer Inc. - ETL Pipeline Challenge (Simulación AWS)

Este proyecto simula una arquitectura serverless completa en AWS para procesar archivos CSV con pedidos de Duff Beer Inc., transformarlos, almacenarlos y exponerlos mediante una API REST. Está desarrollado localmente en Python y Flask, pero documentado como si fuera implementado en AWS.

---


## 🔧ervicios simulados y roles esperados

| Etapa                    | Servicio Simulado (Local) | Equivalente AWS Real          |
|--------------------------|---------------------------|-------------------------------|
| Ingesta de datos         | Carpeta `/data`           | S3 Raw Bucket                 |
| Evento de disparo        | Manual / Simulación       | S3 Trigger (ObjectCreated)    |
| Proceso ETL              | `transform.py` (Pandas)   | Lambda o Glue Job             |
| Validación               | Try/Except + Validación   | Manejo de errores en Lambda   |
| Almacenamiento procesado | Carpeta `/output`         | S3 Processed Bucket           |
| Consulta                 | SQL en CSV                | AWS Athena + Glue Catalog     |
| API REST                 | Flask API (`app.py`)      | API Gateway + Lambda          |

---

## Proceso ETL

1. Lectura del archivo `orders.csv` (simulado desde `/data`)
2. Cálculo de columnas adicionales:
   - `total_price` = `product_price * product_ccf`
3. Agrupación por cliente (`client_id`, `client_name`)
4. Generación de métricas:
   - `total_orders`, `total_sales`
5. Exportación como `.csv` (punto de mejora: usar Parquet)

---

## Testing

Archivo `tests/test_transform.py` incluye pruebas básicas unitarias:

```python
def test_total_price():
    assert calcular_total(10, 3) == 30
```

---

## Consultas SQL (simuladas para Athena)

```sql
-- Total de pedidos por cliente
SELECT client_id, client_name, total_orders FROM orders_summary;

-- Total de ventas por producto
SELECT product_id, SUM(product_price * product_ccf) AS total_sales
FROM orders
GROUP BY product_id;

-- Estado de los pedidos
SELECT status, COUNT(*) FROM orders GROUP BY status;
```

---

## API REST simulada

### Endpoint implementado:

- `GET /orders/<client_id>` → retorna todos los pedidos de un cliente

### Endpoints recomendados para agregar:
- `GET /ventas/producto/<product_id>`
- `GET /ordenes/estado/<status>`
- `GET /clientes/top`

---

## Justificación de Tecnologías

| Tecnología | ¿Por qué se eligió? |
|------------|----------------------|
| **Lambda (simulado)** | Serverless, ejecuta procesamiento sin mantener servidores |
| **Athena** | Consulta directa sobre S3, ideal para datos en CSV o Parquet |
| **Glue Catalog** | Permite definir esquema de datos, integrable con Athena |
| **Parquet (opcional)** | Formato columnar, comprimido, más eficiente que CSV |
| **API Gateway** | Serverless, expone funciones Lambda fácilmente como API REST |

---

## 📦 Recomendaciones para producción

- Usar Parquet en lugar de CSV para mejor performance
- Agregar logs estructurados en CloudWatch
- Validar esquema con `pyarrow` o `pydantic`
- Agregar autenticación (IAM o API Keys) en la API

---

## 📁 Estructura del proyecto

```
duff_beer_etl_project/
├── app/                  # API REST Flask
│   └── app.py
├── etl/                  # ETL transformador
│   └── transform.py
├── data/                 # Archivos de entrada simulados
│   └── orders.csv
├── output/               # Datos transformados
│   └── orders_summary.csv
├── tests/                # Pruebas unitarias
│   └── test_transform.py
├── queries/              # SQL para Athena
│   └── consultas.sql
├── arquitectura_duff_beer_etl.png
└── README.md
```

---

## Cronología del proyecto

- Día 1: Diseño de arquitectura
- Día 2: Implementación ETL y simulación Lambda
- Día 3: Desarrollo de API con Flask
- Día 4: Documentación + pruebas
- Día 5: Diagrama y presentación profesional


