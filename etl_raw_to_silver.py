import sys
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, current_timestamp, lit

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

RAW_PATH = "s3://my-datalake-raw1/"
SILVER_PATH = "s3://my-datalake-silver1/"
DLQ_PATH = "s3://my-datalake-dlq/errors/"

try:
    # Read raw CSV
    df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(RAW_PATH)
    )

    # Transformations
    df_clean = (
        df.withColumn("processed_ts", current_timestamp())
          .withColumn("source", lit("raw_csv"))
    )

    # Write parquet to silver, partitioned by event_date
    (
        df_clean.write.mode("append")
        .partitionBy("event_date")
        .parquet(SILVER_PATH)
    )

    print("ETL Job completed successfully.")

except Exception as e:
    print("ERROR:", e)

    # Write bad records to DLQ
    df.write.mode("append").json(DLQ_PATH)

    raise e

job.commit()
