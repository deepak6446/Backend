CREATE EXTERNAL TABLE `sdk_counts_table`(
  `apikey` string, 
  `sdk` string, 
  `device` string, 
  `request_count` bigint)
PARTITIONED BY ( 
  `year` int, 
  `month` int, 
  `day` int, 
  `orgid` string)
STORED AS PARQUET
LOCATION
  's3://your-company-analytics-bucket/processed/sdk_counts/'
TBLPROPERTIES ("parquet.compress"="SNAPPY");


-- sync the partition metadata in the AWS Glue Data Catalog with the actual partition folders present in the S3 location of the table.
MSCK REPAIR TABLE sdk_counts_table;

SELECT
  sdk,
  SUM(request_count) AS total_requests
FROM 
  sdk_counts_table
WHERE
  year = 2023
  AND month = 10
  AND day = 26
  AND orgid = 'org-abc-123'
GROUP BY 
  sdk
ORDER BY 
  total_requests DESC;