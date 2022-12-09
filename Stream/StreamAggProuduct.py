from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import time

kafka_topic_name = "topicA"
kafka_bootstrap_servers = 'kafka:9092'

if __name__ == "__main__":
    print("Welcome !!!")
    print("Stream Data Processing Application Started ...")
    spark = SparkSession \
        .builder \
        .appName("PySpark Structured Streaming with Kafka") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector:10.0.0')\
        .master("local[*]") \
        .getOrCreate()  
    # Construct a streaming DataFrame that reads from test-topic 
    orders_df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic_name) \
        .option("startingOffsets", "latest") \
        .load()\
        .selectExpr("CAST(value AS STRING)") 

    orders_schema = StructType() \
        .add("full_name", StringType()) \
        .add("gender", StringType()) \
        .add("country", StringType()) \
        .add("Product_name", StringType()) \
        .add("Qte", IntegerType()) 
 
    orders_df1 = orders_df.selectExpr("CAST(value AS STRING)")

    orders_df2 = orders_df1\
        .select(from_json(col("value"),orders_schema)\
        .alias("orders"))      

    orders_df3 = orders_df2.select("orders.*")

    analysis =  orders_df3.groupBy("Product_name")\
                .agg({'Qte': 'sum'})\
                .select("Product_name", col("sum(Qte)") \
                .alias("total_order_amount"))
                

    analysis.writeStream\
        .format("mongodb")\
        .queryName("ToMDB")\
        .option("checkpointLocation", "/tmp/pyspark7/")\
        .option("forceDeleteTempCheckpointLocation", "true")\
        .option('spark.mongodb.connection.uri', 'mongodb://root:pass@mongo:27017/?authSource=admin')\
        .option('spark.mongodb.database', 'Analysis')\
        .option('spark.mongodb.collection', 'ProductAmount')\
        .trigger(processingTime="10 seconds")\
        .outputMode("complete")\
        .start().awaitTermination()

    print("Stream Data Processing Application Completed.")

    # 


    