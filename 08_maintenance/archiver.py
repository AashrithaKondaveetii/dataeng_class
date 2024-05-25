import json
import os
from datetime import datetime
from google.cloud import pubsub_v1, storage


path = '/home/aashritk/default_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

project_id = "dataengineering-420322"
subscription_id = "arch-sub"
bucket_name = "maintenance-bucket1"  

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

storage_client = storage.Client(project=project_id)

message_count = 0
all_messages = []

def save_messages_to_file(messages, file_path):
    """Save all messages to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(messages, file)

def upload_to_bucket(file_path, bucket_name, blob_name):
    """Uploads data to the specified bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_path, content_type="application/json")
    print(f"Uploaded data to {bucket_name}/{blob_name}")

def callback(message):
    global message_count, all_messages
    data = message.data.decode('utf-8')
    
    all_messages.append(json.loads(data))
    
    message.ack()
    message_count += 1

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}...")

file_path = 'all_messages.json'

with subscriber:
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

save_messages_to_file(all_messages, file_path)

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
blob_name = f"messages/{timestamp}.json"

upload_to_bucket(file_path, bucket_name, blob_name)

print(f"Total messages received: {message_count}")
