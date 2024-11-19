from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import os
import boto3

def calculate_journey_length(taxi_df):
    '''
    Calculate the journey length
    Parameters: taxi_df: pyspark.sql.dataframe.DataFrame
    Returns: taxi_journey: pyspark.sql.dataframe.DataFrame
    '''

    taxi_journey = taxi.withColumn('journey_length', (F.unix_timestamp(F.col("tpep_dropoff_datetime")) - F.unix_timestamp(F.col("tpep_pickup_datetime")))/60)

    print("longest_journey", taxi_journey.orderBy(taxi_journey['journey_length'].desc()).select('VendorID', 'journey_length').show(3))
    print("shortest_journey", taxi_journey.orderBy(taxi_journey['journey_length']).select('VendorID', 'journey_length').show(3))

    return taxi_journey

def calculate_tip_percentage(taxi_df):
    '''
    Calculate the tip percentage
    Parameters: taxi_df: pyspark.sql.dataframe.DataFrame
    Returns: taxi_journey: pyspark.sql.dataframe.DataFrame
    '''

    taxi_journey = taxi.withColumn('tip_percent', F.col('tip_amount')/(F.col('fare_amount')+F.col('extra')+F.col('mta_tax')+F.col('improvement_surcharge')+F.col('tolls_amount'))*100)

    print("highest tippers", taxi_journey.orderBy(taxi_journey['tip_percent'].desc()).select('VendorID', 'tip_percent', 'tip_amount').show(3))
    print("lowest tippers", taxi_journey.orderBy(taxi_journey['tip_percent']).select('VendorID', 'tip_percent', 'tip_amount').show(3))

    return taxi_journey

access_key = os.getenv("access_key")

client = boto3.client('secretsmanager')
get_secret_value_response = client.get_secret_value(SecretId="s3-user")
secret_key = get_secret_value_response['SecretString']

spark = SparkSession.builder.appName("transformation").config("spark.hadoop.fs.s3a.access.key", access_key) \
    .config("spark.hadoop.fs.s3a.secret.key", secret_key) \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0,org.apache.hadoop:hadoop-aws:3.3.2") \
    .config("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.jars", "/path/to/hadoop-aws-X.X.X.jar,/path/to/aws-java-sdk-bundle-X.X.X.jar") \
    .getOrCreate()
taxi = spark.read.parquet('data/yellow_tripdata_2024-01.parquet')

taxi.printSchema()

taxi_journey = calculate_journey_length(taxi)

taxi_journey = calculate_tip_percentage(taxi_journey)

taxi_journey.write.parquet("s3a://my-taxi-bucket-1/yellow_tripdata_2024-01_journeys.parquet")

spark.stop()