import random
import json
from kafka import KafkaConsumer
import pandas as pd
import joblib


model = joblib.load("model.pkl")

def create_consumer():
    """Create a connection to Kafka broker as a consumer"""
    consumer = KafkaConsumer(
        'transactions',                          # Topic to subscribe to
        bootstrap_servers=['localhost:9092'],
        # Convert JSON bytes to Python dict
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        # Start reading from the beginning of the topic
        auto_offset_reset='earliest'
    )
    return consumer


def is_fraud(transaction):
    amount = transaction["amount"]
    location = transaction["location"]
    device = transaction["device"]

    high_risk_locations = ["bangkok", "istanbul", "sao paulo", "mexico city"]

    risk_score = 0

    if amount > 800:
        risk_score += 0.6
    elif amount > 500:
        risk_score += 0.3
    elif amount > 300:
        risk_score += 0.1

    
    if location.lower() in high_risk_locations:
        risk_score += 0.3

    
    if device == "tablet":
        risk_score += 0.2
    elif device == "web":
        risk_score += 0.1

    if amount > 500 and device == "mobile":
        risk_score += 0.2

    if location.lower() in high_risk_locations and amount > 400:
        risk_score += 0.3

    # 🔥 Decisión con probabilidad
    probability = min(risk_score, 0.95)  # cap para no llegar a 100%

    return random.random() < probability

def process_transaction(transaction):
    """Simple function to process an transaction (just prints it in this example)"""
    print(f"Processing transaction of user_id: {transaction['user_id']} for {transaction['amount']} $$$$")

    df = pd.DataFrame([transaction])

    df = pd.get_dummies(df)

    df = df.reindex(columns=model.feature_names_in_, fill_value=0)
 
    prediction = model.predict(df)[0]

    if prediction == 1:
        print("🚨 FRAUD DETECTED")
    else:
        print("✅ NORMAL")

    # if(is_fraud(transaction)):
    #     transaction["is_suspect"] = True

    # df1 = pd.DataFrame([transaction])

    # try:
    #     df2 = pd.read_parquet("data.parquet")
    # except:
    #     df2 = pd.DataFrame() 

    # df = pd.concat([df2, df1], axis=0)

    # df.to_parquet("data.parquet")

def run_consumer():
    """Run the consumer, reading messages"""
    consumer = create_consumer()
    
    try:
        print("Consumer started. Waiting for messages...")
        # Continuously poll for new messages
        for message in consumer:
            transaction = message.value
            process_transaction(transaction)
            print("---")
    except KeyboardInterrupt:
        print("Consumer stopped by user")
    finally:
        consumer.close()
        print("Consumer closed")

# Main execution
if __name__ == "__main__":

    run_consumer()