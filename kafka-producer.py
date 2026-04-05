import json
from kafka import KafkaProducer
import time
import random

def create_producer():
    """Create a connection to Kafka broker"""
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        # Convert Python dict to JSON string and encode as bytes
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    return producer

def send_transaction(producer, transactionId):
    """Send a simple transaction message to Kafka"""
    # Create a sample transaction message
    locations = [
        "New York", "London", "Tokyo", "Paris", "Berlin",
        "Madrid", "Rome", "Toronto", "Sydney", "Dubai",
        "Singapore", "Hong Kong", "Mexico City", "São Paulo",
        "Buenos Aires", "Cape Town", "Mumbai", "Seoul", "Bangkok", "Istanbul"
    ]
    devices = ["mobile", "web", "tablet"] 

    transaction = {
        "user_id": transactionId,
        "amount": random.randint(10, 200) * 5.3,
        "location": random.choice(locations),
        "device": random.choice(devices)
    }
    
    # Send the transaction to the 'transactions' topic
    # The transactionId (as string) is used as the message key
    producer.send(
        'transactions',                         # Topic name
        key=str(transactionId).encode('utf-8'),  # Message key (optional)
        value=transaction                       # Message value
    ).get() # el get fuerza a que kafka confirme envio
    print(f"Sent transaction: {transaction}")
    

def run_producer():
    """Run the producer, sending a few messages"""
    producer = create_producer()
    
    try:
        # Send 10 transaction messages
        for i in range(1000):
            send_transaction(producer, i)
            time.sleep(0.1) 
    finally:
        # Always flush and close the producer when done
        producer.flush()
        producer.close()
        print("Producer closed")
# Main execution
if __name__ == "__main__":
    # To run as a producer, uncomment:
    run_producer()