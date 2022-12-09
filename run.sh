#docker-compose up -d 
ConatinerKafka="kafka"
ConatinerSpark="spark"
# Create Analysis database on Mongodb

#Create Topic 
cmd1="kafka-topics.sh --create --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1 --topic topicA"

# Start Stream App
cmd2="spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0 /data/StreamAggCountry.py"

cmd3="spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0 /data/StreamAggProuduct.py"

cmd4="spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0,org.mongodb.spark:mongo-spark-connector:10.0.0  /data/StreamAggGender.py "

#uncomment app in docker-cmpose and rerun docker-compose to start the app that will sent the data into kafka evry 10 seconds 


docker exec -u 0 $ConatinerKafka bash -c "$cmd1 && $cmd2"

docker exec -u 0 $ConatinerSpark bash -c "$cmd3"

docker exec -u 0 $ConatinerSpark bash -c "$cmd4"

#run the Dashbord python -m streamlit run .\2_??_Dash.py