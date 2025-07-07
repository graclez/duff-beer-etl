
# Simulación del Proyecto en AWS (Arquitectura Serverless)

Este documento explica cómo se implementaría **exactamente el mismo pipeline ETL** en un entorno real de **AWS**, siguiendo todos los requerimientos del desafío.

---

## 1. Ingesta de Datos (Amazon S3)

- Se crea un bucket llamado: `duffbeer-input-orders`
- Los archivos `.csv` con los pedidos son subidos manual o automáticamente a este bucket.
- Este archivo es la **fuente de datos inicial** del proceso ETL.

---

## 2. Disparador de Evento (Trigger S3 → Lambda)

- En el bucket `duffbeer-input-orders`, se configura una **notificación de evento `s3:ObjectCreated:*`**.
- Este evento activa automáticamente una **AWS Lambda** que inicia el flujo de ETL.
- Alternativamente, esta Lambda puede invocar una **AWS Step Function**.

---

## 3. Proceso ETL

### Opción A: Usando Step Functions + Lambda (Recomendado)
- **Paso 1:** Lambda valida que el archivo sea correcto (extensión, columnas, tamaño).
- **Paso 2:** Otra Lambda lee el archivo desde S3 y realiza la transformación:
    - Calcula total de ventas por cliente.
    - Total por producto y canal.
    - Limpia y valida los datos.
- **Paso 3:** Guarda los datos transformados en un segundo bucket: `duffbeer-processed-orders`.

### Opción B: Usando AWS Glue (escalable)
- Se crea un **Glue Job en PySpark** que:
    - Lee el CSV desde `s3://duffbeer-input-orders/`
    - Procesa la información (como lo hace el script de ETL local)
    - Guarda el resultado en formato Parquet o CSV en `s3://duffbeer-processed-orders/`

---

## 4. Almacenamiento y Consultas (Athena)

- Se crea una base de datos en el catálogo de Glue.
- Se define una tabla externa que apunta a `s3://duffbeer-processed-orders/`
- Se puede consultar desde Athena con SQL directamente:
    ```sql
    SELECT client_id, COUNT(*) AS total_orders
    FROM processed_orders
    GROUP BY client_id;
    ```

---

## 5. API REST (API Gateway + Lambda)

- Se crea una API REST con Amazon API Gateway.
- Cada endpoint invoca una Lambda que:
    - Lee desde Athena (usando Boto3)
    - O desde los archivos S3 procesados
- Endpoints típicos:
    - `GET /orders/{client_id}`
    - `GET /sales-by-product`
    - `GET /order-status-report`

---

## 6. Manejo de Errores y Logs

- Todas las Lambdas registran logs en **CloudWatch**.
- Se puede configurar alertas si hay fallos en Glue, S3 o Lambda.

---

## 7. Optimización

- Se recomienda guardar los datos transformados en **Parquet**, particionado por fecha o canal de venta.
- Glue y Athena soportan archivos grandes y consultas optimizadas.
- Se pueden usar **Athena Workgroups** para controlar costos.

---

## Arquitectura General

```text
[S3: duffbeer-input-orders]
      ↓ trigger
[Lambda (o Step Function)]
      ↓
[Transformación con Lambda o Glue]
      ↓
[S3: duffbeer-processed-orders]
      ↓
[Athena]
      ↓
[API Gateway] → [Usuarios / Dashboards]
```

---

Este archivo simula que el proyecto fue pensado para ejecutarse completamente en AWS, aunque esté implementado localmente.

