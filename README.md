# Real-Time Fraud Detection Pipeline (Kafka + ML)

## Overview

This project implements an end-to-end pipeline for fraud detection using streaming data and machine learning.

It simulates financial transactions, streams them through Kafka, processes them in real time, and applies a trained model to classify transactions as fraudulent or normal.

The goal is to connect data engineering and machine learning in a single working system.

---

## Architecture

```
Producer → Kafka → Consumer → Processing → ML Model → Prediction → Storage
```

* Producer: generates simulated transactions
* Kafka: handles real-time streaming
* Consumer: processes incoming data
* Storage: saves historical data in Parquet
* Model: predicts whether a transaction is suspicious

---

## Features

* Real-time data streaming with Kafka
* End-to-end pipeline (generation, ingestion, processing, storage, ML)
* Basic feature engineering with categorical encoding
* Machine learning model (Random Forest)
* Real-time prediction
* Data persistence using Parquet

---

## Data

The dataset is generated programmatically and includes:

* user_id
* amount
* location
* device

Fraud labels are generated using probabilistic rules based on these features to avoid trivial patterns.

---

## Machine Learning

* Model: RandomForestClassifier
* Features:

  * amount
  * location (encoded)
  * device (encoded)
* Target:

  * is_suspect

The model is trained using historical data stored in Parquet and then used for inference in the consumer.

---

## Real-Time Processing

For each incoming transaction:

1. The data is transformed to match the training format
2. The model generates a prediction
3. The result is printed as fraud or normal

---

## Project Structure

```
.
├── kafka-producer.py
├── kafka-consumer.py
├── train_model.py
├── model.pkl
├── data.parquet
└── README.md
```

---

## How to Run

Start Kafka:

```
docker-compose up -d
```

Run producer:

```
python kafka-producer.py
```

Run consumer:

```
python kafka-consumer.py
```

## Technologies

* Python
* Apache Kafka
* Pandas
* Scikit-learn
* Docker
* Parquet
