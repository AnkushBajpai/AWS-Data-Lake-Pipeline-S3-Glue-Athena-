# AWS Data Lake Pipeline – Raw → Silver (Parquet)

This project demonstrates a fully functional AWS Data Lake Pipeline using:

- Amazon S3 (Raw, Silver, and DLQ layers)
- AWS Glue Crawler (Schema detection)
- AWS Glue Spark ETL Job (Transformations, schema cleanup, Parquet output)
- Amazon Athena (Validation and SQL analytics)
- CloudWatch Logs (Monitoring)

## Architecture Overview

End‑to‑end pipeline:
1. Data uploaded to **Raw S3 bucket**
2. Glue Crawler creates schema → raw_db
3. Glue ETL job:
   - Reads CSV from Raw
   - Cleans and transforms data
   - Writes partitioned Parquet to Silver
   - Sends bad records to DLQ
4. Athena external table reads Silver Parquet

## Project Structure
```
├── etl_raw_to_silver.py
├── architecture_diagram.png
├── sample_data/
├── Glue_json_config/
└── README.md
```

## 1. Setup S3 Buckets

- my-datalake-raw1  
- my-datalake-silver1  
- my-datalake-dlq  

## 2. Glue Crawler

Configure the crawler to scan **my-datalake-raw1** and create **raw_db**.

## 3. Glue ETL Script

PySpark script performs:
- Read raw CSV
- Add metadata columns
- Convert event_date → date
- Write Parquet partitioned by event_date

## 4. Athena Table

Create an external parquet table on Silver:
```
MSCK REPAIR TABLE my_silver_table;
```

## 5. Validation Queries
Run Athena queries for validation.

## 6. Error Handling
Malformed records go to the **DLQ bucket**.

## 7. Logging & Monitoring
CloudWatch Logs & Glue job metrics.

## 8. Enhancements
Future additions: Gold layer, workflows, triggers, dashboards.

## Author
Ankush Bajpai
