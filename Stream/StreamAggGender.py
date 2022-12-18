from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import time

kafka_topic_name = "topicA"
kafka_bootstrap_servers = 'kafka:9092'

if __name__ == "__main__":
    print("Welcome !!!")
    print("Stream Agg Gender..")
    spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.0')\
        .master("local[*]") \
        .getOrCreate()  
    # Construct a streaming DataFrame that reads from topic 
    orders_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic_name) \
        .option("startingOffsets", "latest") \
        .load()\
        .selectExpr("CAST(value AS STRING)") 


    orders_schema = StructType() \
        .add("id", IntegerType())\
        .add("first_name", StringType()) \
        .add("last_name", StringType()) \
        .add("country", StringType()) \
        .add("Product_name", StringType()) \
        .add("gender", StringType()) \
        .add("quantity", IntegerType()) 

    orders_df1 = orders_df\
        .select(from_json(col("value"),orders_schema)\
        .alias("orders"))\
        .select("orders.*")

    analysis =  orders_df1.groupBy("gender")\
                .agg({'quantity': 'sum'})\
                .select("gender", col("sum(quantity)") \
                .alias("total_order_amount"))

    analysis.writeStream\
        .format("mongodb")\
        .queryName("ToMDB")\
        .option("checkpointLocation", "/tmp/pyspark5/")\
        .option("forceDeleteTempCheckpointLocation", "true")\
        .option('spark.mongodb.connection.uri', 'mongodb://root:pass@mongo:27017/?authSource=admin')\
        .option('spark.mongodb.database', 'Analysis')\
        .option('spark.mongodb.collection', 'GenderAmount')\
        .trigger(processingTime="10 seconds")\
        .outputMode("complete")\
        .start().awaitTermination()

    print("Stream Data Processing Application Completed.")

    # spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0 app.py



    