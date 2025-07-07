
# Implementación completa en AWS – Duff Beer ETL Pipeline (Simulación)

Este documento detalla paso a paso cómo se implementó el pipeline ETL para Duff Beer Inc. **como si se hubiera desplegado en AWS real**, siguiendo una arquitectura totalmente serverless.

---

## 🧱 Servicios utilizados:

- **Amazon S3**: Ingesta y almacenamiento
- **AWS Lambda**: Procesamiento ETL
- **AWS Step Functions**: Orquestación (opcional)
- **AWS Glue**: Transformación escalable (opcional)
- **AWS Glue Catalog**: Catálogo de metadatos
- **Amazon Athena**: Consultas SQL
- **Amazon API Gateway**: Exposición de datos vía API
- **Amazon CloudWatch**: Logs y monitoreo
- **IAM**: Permisos y roles

---

## ✅ PASOS EN AWS

### 1. Creación de Buckets en S3

- `duffbeer-input-orders`: recibe archivos .csv de pedidos
- `duffbeer-processed-orders`: almacena los resultados transformados

```bash
aws s3 mb s3://duffbeer-input-orders
aws s3 mb s3://duffbeer-processed-orders
```

---

### 2. Configuración del trigger en S3

- Al subir el archivo al bucket `duffbeer-input-orders`, se dispara una función Lambda

```json
{
  "LambdaFunctionConfigurations": [
    {
      "Id": "TriggerETL",
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:123456789012:function:start_etl",
      "Events": ["s3:ObjectCreated:*"]
    }
  ]
}
```

---

### 3. Función Lambda – Validación y procesamiento inicial

- La función `start_etl` valida el archivo (formato y columnas)
- Luego invoca directamente una función `process_orders_lambda`
- O inicia una **Step Function** que orquesta todo

---

### 4. AWS Step Functions – Flujo del proceso ETL (opcional)

- Flujo compuesto por:
  - Paso 1: Validar CSV
  - Paso 2: Transformar (con otra Lambda)
  - Paso 3: Guardar resultado en `duffbeer-processed-orders`

---

### 5. Lambda de transformación (o Glue Job)

- Lee el CSV desde S3
- Realiza cálculos:
  - Total ventas por cliente
  - Total por producto y canal
- Limpia y estructura los datos
- Escribe resultado en otro bucket como `.csv` o `.parquet`

---

### 6. Glue Data Catalog + Athena

- Crea base de datos y tabla externa en Glue:

```sql
CREATE EXTERNAL TABLE duffbeer_reports.orders_summary (
    client_id INT,
    client_name STRING,
    total_orders INT,
    total_sales DOUBLE
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION 's3://duffbeer-processed-orders/';
```

- Consultas disponibles:
  - Total pedidos por cliente
  - Ventas por producto
  - Estados de pedidos (delivered, broken, created)

---

### 7. API REST con API Gateway + Lambda

- Crear una REST API en API Gateway con rutas:
  - `/orders/{client_id}`
  - `/sales-by-product`
  - `/order-status-report`
- Cada ruta llama a una Lambda que consulta Athena o lee desde S3
- Devuelve los resultados en JSON

---

### 8. Monitoreo y Logs

- Todos los eventos (Lambda, errores, ejecuciones) son enviados a CloudWatch Logs
- Alarmas configuradas si falla alguna ejecución crítica

---

### 9. Seguridad y permisos

- Cada Lambda tiene su rol IAM con:
  - Permiso `s3:GetObject` y `s3:PutObject`
  - Permiso `athena:StartQueryExecution`
  - Permiso `glue:GetTable`, `glue:GetDatabase`

---

### 10. Optimización

- Se guardan los archivos transformados en Parquet
- Se particiona por canal de venta y fecha
- Athena consulta datasets optimizados para reducir costos

