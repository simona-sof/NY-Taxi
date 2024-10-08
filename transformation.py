from pyspark.sql import SparkSession
import pyspark.sql.functions as F

# Replace with your own access key and secret key
spark = SparkSession.builder.appName("transformation").config("spark.hadoop.fs.s3a.access.key", "ACCESS KEY") \ 
    .config("spark.hadoop.fs.s3a.secret.key", "SECRET KEY") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.3.0,org.apache.hadoop:hadoop-aws:3.3.2") \
    .config("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.jars", "/path/to/hadoop-aws-X.X.X.jar,/path/to/aws-java-sdk-bundle-X.X.X.jar") \
    .getOrCreate()
taxi = spark.read.parquet('data/yellow_tripdata_2024-01.parquet')

taxi.printSchema()

# Calculate the journey length
taxi_journey = taxi.withColumn('journey_length', (F.col("tpep_dropoff_datetime") - F.col("tpep_pickup_datetime")).cast("long")/60)

print("longest_journey", taxi_journey.orderBy(taxi_journey['journey_length'].desc()).select('VendorID', 'journey_length').show(3))
print("shortest_journey", taxi_journey.orderBy(taxi_journey['journey_length']).select('VendorID', 'journey_length').show(3))

# Calculate the tip percentage
taxi_journey = taxi.withColumn('tip_percent', F.col('tip_amount')/(F.col('fare_amount')+F.col('extra')+F.col('mta_tax')+F.col('improvement_surcharge')+F.col('tolls_amount'))*100)

print("highest tippers", taxi_journey.orderBy(taxi_journey['tip_percent'].desc()).select('VendorID', 'tip_percent', 'tip_amount').show(3))
print("lowest tippers", taxi_journey.orderBy(taxi_journey['tip_percent']).select('VendorID', 'tip_percent', 'tip_amount').show(3))

taxi_journey.write.parquet("s3a://my-taxi-bucket-1/yellow_tripdata_2024-01_journeys.parquet")