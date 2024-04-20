                                                                                     
import requests
import json
import os
from google.cloud import pubsub_v1

def fetch_data(vehicle_ids):
    all_data = []
    for vehicle_id in vehicle_ids:
        response = requests.get(f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}")
        if response.status_code == 200:
            all_data.extend(response.json())
        else:
            print(f"Failed to fetch data for vehicle ID {vehicle_id}: {response.status_code}")
    return all_data

def save_data_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file)
    print("Data fetched and saved to", filename)

def read_data_from_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def publish_data_to_pubsub(data, publisher, topic_path):
    msg_count = 0
    for record in data:
        data_str = json.dumps(record)
        data_bytes = data_str.encode("utf-8")
        future = publisher.publish(topic_path, data_bytes)
        print(f"Published message ID: {future.result()}")
        msg_count += 1
    print(f"All records have been published to {topic_path}. Total messages: {msg_count}")

def main():

    credential_path = '/home/aashritk/default_credentials.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    # Vehicle IDs to fetch data for
    vehicle_ids = ['3901', '3319']
    data_file = 'bcsample.json'

    # Fetch and save data
    data = fetch_data(vehicle_ids)
    save_data_to_file(data, data_file)

    # Set up Google Pub/Sub
    project_id = "dataengineering-420322"
    topic_id = "my-topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    # Publish data
    data_to_publish = read_data_from_file(data_file)
    publish_data_to_pubsub(data_to_publish, publisher, topic_path)

if __name__ == '__main__':
    main()