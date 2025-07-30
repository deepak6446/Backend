"""
Spark job to process daily Fastly logs.
- Reads raw JSON logs from an S3 source.
- Aggregates SDK usage counts by org, API key, etc.
- Writes aggregated data to S3 in partitioned Parquet format for Athena.
"""

from pyspark.sql import SparkSession, functions as F
from shared.udfs import parse_user_agent_udf
from shared.logger import get_logger # Assuming you have a logger utility

def run_job(spark: SparkSession, config: dict, process_date: str):
    """
    Executes the Fastly log processing job for a given date.

    Args:
        spark: The SparkSession object.
        config: A dictionary with the application configuration.
        process_date: The date to process in 'YYYY-MM-DD' format.
    """
    log = get_logger(spark, "FastlyLogProcessor")
    job_config = config['fastly_processor']

    log.info("Starting Fastly log processing job for date: %s", process_date)

    # 1. Define Input and Output Paths from config
    input_path = (
        f"s3a://{job_config['source_bucket']}/"
        f"{job_config['source_data_path']}/date={process_date}/"
    )
    output_path = (
        f"s3a://{job_config['dest_bucket']}/"
        f"{job_config['dest_data_path']}/"
    )

    log.info("Reading raw logs from: %s", input_path)
    log.info("Writing processed data to: %s", output_path)

    # 2. Read Raw Logs
    raw_df = spark.read.json(input_path)

    # 3. Process and Transform Data
    processed_df = (
        raw_df
        .withColumn("orgId", F.col("request_headers.X-Org-ID"))
        .withColumn("apiKey", F.col("request_headers.X-Api-Key"))
        .select("timestamp", "user_agent", "orgId", "apiKey")
        .withColumn("orgId", F.coalesce(F.col("orgId"), F.lit("unknown")))
        .withColumn("apiKey", F.coalesce(F.col("apiKey"), F.lit("unknown")))
        .withColumn("year", F.year(F.to_date(F.col("timestamp"))))
        .withColumn("month", F.month(F.to_date(F.col("timestamp"))))
        .withColumn("day", F.dayofmonth(F.to_date(F.col("timestamp"))))
        .withColumn("agent_details", parse_user_agent_udf(F.col("user_agent")))
        .withColumn("sdk", F.col("agent_details.sdk"))
        .withColumn("device", F.col("agent_details.device"))
        .drop("timestamp", "user_agent", "agent_details")
    )

    # 4. Aggregate Data
    aggregated_df = (
        processed_df
        .groupBy("year", "month", "day", "orgId", "apiKey", "sdk", "device")
        .count()
        .withColumnRenamed("count", "request_count")
    )

    # 5. Write to S3 in Partitioned Parquet Format
    log.info("Writing aggregated data with partitions...")
    (
        aggregated_df.write
        .mode("append")
        .partitionBy("year", "month", "day", "orgId")
        .parquet(output_path)
    )

    log.info("Successfully finished Fastly log processing job.")