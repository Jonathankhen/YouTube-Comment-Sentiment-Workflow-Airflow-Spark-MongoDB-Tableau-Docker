from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType
from textblob import TextBlob

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("YouTubeSentimentAnalysis") \
    .config("spark.mongodb.output.uri", "mongodb://mongodb:27017/youtube.sentiment") \
    .getOrCreate()

# Define schema for the data
schema = StructType([
    StructField("text", StringType(), True),
    StructField("user", StringType(), True),
    StructField("timestamp", StringType(), True)
])

# Read data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "youtube-comments-stream") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

json_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Define a UDF for sentiment analysis
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

spark.udf.register("get_sentiment", get_sentiment)

# Perform sentiment analysis
processed_df = json_df.withColumn("sentiment", get_sentiment(col("text")))

# Write processed data to MongoDB
query = processed_df.writeStream \
    .format("mongo") \
    .option("uri", "mongodb://mongodb:27017/youtube.sentiment") \
    .option("checkpointLocation", "/tmp/checkpoints") \
    .outputMode("append") \
    .start()

query.awaitTermination()
