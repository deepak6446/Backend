"""
Main entry point for submitting Spark jobs.
"""
import argparse
import json
from pyspark.sql import SparkSession

# Assuming your project structure allows these imports
from jobs.ui import run_job as run_ui_job
from jobs.fastly_log_processor import run_job as run_fastly_job # NEW
from shared.logger import get_logger

def main():
    """
    Parses arguments and launches the requested Spark job.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--job", required=True, choices=['ui', 'fastly_processor'], help="Name of the job to run.") # ADDED fastly_processor
    parser.add_argument("--start_date", required=True, help="Start date (YYYY-MM-DD). For daily jobs, this is the process date.")
    # ... other arguments like --end_date if needed

    args = parser.parse_args()

    # Load configuration
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    # Initialize Spark Session
    spark = (
        SparkSession.builder.appName(f"DataProcessing-{args.job}-{args.start_date}")
        .getOrCreate()
    )
    
    log = get_logger(spark, "Main")
    log.info("Launching job '%s' for date '%s'", args.job, args.start_date)

    # Job runner logic
    if args.job == 'ui':
        run_ui_job(spark, config, args.start_date)
    # --- NEW BLOCK TO RUN THE FASTLY JOB ---
    elif args.job == 'fastly_processor':
        # For this daily job, start_date is the only date we need.
        run_fastly_job(spark, config, args.start_date)
    # -------------------------------------
    else:
        log.error("Job '%s' is not a valid job name.", args.job)

    log.info("Job execution complete.")
    spark.stop()


if __name__ == "__main__":
    main()