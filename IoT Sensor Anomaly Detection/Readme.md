# IoT Sensor Anomaly Detection System

A Python-based streaming data pipeline that uses machine learning to detect anomalies in IoT sensor data. The system processes real-time data from Kafka, detects anomalies using an Isolation Forest model, and stores results in an Amazon S3 bucket.

---

## Features

- **Real-Time Streaming**: Consumes data from a Kafka topic for continuous monitoring.
- **Anomaly Detection**: Leverages an Isolation Forest model to identify anomalies in IoT sensor data.
- **Scalable Processing**: Uses Apache Spark for distributed data processing.
- **S3 Integration**: Saves detected anomalies in Parquet format for further analysis.

---

## Project Structure

### 1. `anomaly_detection.py`
- Implements the anomaly detection pipeline.
- Key Functions:
  - `train_isolation_forest(data)`: Trains the Isolation Forest model using historical data.
  - `read_kafka_stream(servers, topic)`: Reads real-time data from a Kafka topic.
  - `parse_kafka_data(df, schema)`: Parses raw Kafka messages into structured data.
  - `assemble_features(df)`: Prepares feature columns for anomaly detection.
  - `predict_anomalies(batch_df, batch_id, model)`: Identifies anomalies in each batch and saves them to S3.
  - `main(kafka_bootstrap_servers, kafka_topic, historical_data)`: Orchestrates the pipeline.

---

## Setup & Usage

### Prerequisites
- **Environment**: Python 3.9+, Apache Spark, Kafka, and AWS S3.
- **Required Python Libraries**:
  - `pyspark`, `pandas`, `scikit-learn`, `boto3`
- Install dependencies:
  ```bash
  pip install pyspark pandas scikit-learn boto3
