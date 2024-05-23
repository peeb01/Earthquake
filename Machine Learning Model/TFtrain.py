from pyspark.sql import SparkSession
import warnings

with warnings.catch_warnings():
    warnings.filterwarnings("ignore")


spark = SparkSession.builder \
    .appName("Read CSV with PySpark") \
    .getOrCreate()

csv_file_path = "DATASET_STORE\\UPDATE DATASET_1.csv"

df = spark.read.csv(csv_file_path, header=True, inferSchema=True)

df = df.toPandas()
print(df.head())