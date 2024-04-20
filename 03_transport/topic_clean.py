from google.cloud import pubsub_v1
import os


path = '/home/aashritk/default_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path


project_id = "dataengineering-420322"
subscription_id = "my-sub"


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    
    message.ack()
    print(f"Message discarded: {message.message_id}")

def main():
    print(f"Listening for messages on {subscription_path} to discard them...\n")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    
    with subscriber:
        try:
            
            streaming_pull_future.result(timeout=30)  
        except TimeoutError:
            streaming_pull_future.cancel()  
            streaming_pull_future.result()  

        print("No more messages to discard, or timeout reached.")

if __name__ == '__main__':
    main()