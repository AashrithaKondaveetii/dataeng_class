from google.cloud import pubsub_v1
import json
import os 

path = '/home/aashritk/default_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

project_id = "dataengineering-420322"
topic_id = "my-topic"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)


with open('bcsample.json', 'r') as file:
    data_records = json.load(file)
msg_count = 0

for record in data_records:
    
    data_str = json.dumps(record)
    data = data_str.encode("utf-8")
    
    future = publisher.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")
    msg_count += 1



print(f"All records have been published to {topic_path} and message count is: {msg_count}")