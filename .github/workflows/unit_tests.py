import unittest
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

class TransformationTests(unittest.TestCase):
    def setUp(self):
        self.spark = SparkSession.builder.master("local").appName("TransformationTests").getOrCreate()
        self.taxi_data = [
            (1, "2024-01-01 00:00:00", "2024-01-01 00:10:00", 10.0, 2.0, 1.0, 0.5, 0.0, 2.7),
            (2, "2024-01-01 00:00:00", "2024-01-01 00:05:00", 5.0, 1.0, 0.5, 0.25, 0.0, 1.35),
            (3, "2024-01-01 00:00:00", "2024-01-01 00:15:00", 15.0, 3.0, 1.5, 0.75, 0.0, 4.05)
        ]
        self.taxi_df = self.spark.createDataFrame(self.taxi_data, ["VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "fare_amount", "extra", "mta_tax", "improvement_surcharge", "tolls_amount", "tip_amount"])

    def tearDown(self):
        self.spark.stop()

    def test_journey_length(self):
        transformed_df = self.taxi_df.withColumn('journey_length', (F.unix_timestamp(F.col("tpep_dropoff_datetime")) - F.unix_timestamp(F.col("tpep_pickup_datetime")))/60)
        expected_df = self.spark.createDataFrame([
            (1, "2024-01-01 00:00:00", "2024-01-01 00:10:00", 10.0, 2.0, 1.0, 0.5, 0.0, 2.7, 10.0),
            (2, "2024-01-01 00:00:00", "2024-01-01 00:05:00", 5.0, 1.0, 0.5, 0.25, 0.0, 1.35, 5.0),
            (3, "2024-01-01 00:00:00", "2024-01-01 00:15:00", 15.0, 3.0, 1.5, 0.75, 0.0, 4.05, 15.0)
        ], ["VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "fare_amount", "extra", "mta_tax", "improvement_surcharge", "tolls_amount", "tip_amount", "journey_length"])
        self.assertEqual(transformed_df.collect(), expected_df.collect())

    def test_tip_percentage(self):
        transformed_df = self.taxi_df.withColumn('tip_percent', F.col('tip_amount')/(F.col('fare_amount')+F.col('extra')+F.col('mta_tax')+F.col('improvement_surcharge')+F.col('tolls_amount'))*100)
        expected_df = self.spark.createDataFrame([
            (1, "2024-01-01 00:00:00", "2024-01-01 00:10:00", 10.0, 2.0, 1.0, 0.5, 0.0, 2.7, 20.0),
            (2, "2024-01-01 00:00:00", "2024-01-01 00:05:00", 5.0, 1.0, 0.5, 0.25, 0.0, 1.35, 20.0),
            (3, "2024-01-01 00:00:00", "2024-01-01 00:15:00", 15.0, 3.0, 1.5, 0.75, 0.0, 4.05, 20.0)
        ], ["VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "fare_amount", "extra", "mta_tax", "improvement_surcharge", "tolls_amount", "tip_amount", "tip_percent"])
        self.assertEqual(transformed_df.collect(), expected_df.collect())
        
if __name__ == '__main__':
    unittest.main()