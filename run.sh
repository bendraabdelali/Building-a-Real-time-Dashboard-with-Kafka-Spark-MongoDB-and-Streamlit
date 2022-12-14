#docker-compose up -d 
ConatinerKafka="kafka"
ConatinerSpark="spark"
# Create an analysis database on MongoDB by accessing a MongoDB admin using this URL: localhost:8081 and give 'mexpress' as the username and password

#Create Topic 
docker exec -u 0 kafka bash -c "kafka-topics.sh --create --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 --topic topicA"

# Start Stream App
docker exec -u 0 kafka bash -c "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0 /data/StreamAggCountry.py"

docker exec -u 0 kafka bash -c "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0 /data/StreamAggProuduct.py"

docker exec -u 0 kafka bash -c "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0  /data/StreamAggGender.py "

# start Ecommerce data generator
cd Ecommerce\ data\ generator
python producer.py

#run the Dashbord 
python -m streamlit run Dashboard/dashboard.py