import requests
import json
import os

path = '\home\aashritk\default_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path

vehicle_ids = ['3901', '4302']

all_data = []
for vehicle_id in vehicle_ids:
    response = requests.get(f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}")
    if response.status_code == 200:
        all_data.extend(response.json())

with open('bcsample.json', 'w') as f:
    json.dump(all_data, f)

print("Data fetched and saved to bcsample.json")