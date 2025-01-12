from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.ml.feature import VectorAssembler
from sklearn.ensemble import IsolationForest
import pandas as pd

# Initialize Spark session
spark = SparkSession.builder \
    .appName("IoT Sensor Anomaly Detection") \
    .getOrCreate()

# Define schema for the IoT sensor data
schema = """
    device_id STRING,
    timestamp STRING,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT
"""

def train_isolation_forest(data):
    """
    Trains the Isolation Forest model for anomaly detection.

    Args:
    - data (pandas.DataFrame): A DataFrame containing the sensor data used to train the model.
    
    Returns:
    - IsolationForest: A trained Isolation Forest model.
    """
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(data)
    return model

# Read streaming data from Confluent Kafka topic
def read_kafka_stream(kafka_bootstrap_servers, kafka_topic):
    """
    Reads a streaming data from Confluent Kafka topic.

    Args:
    - kafka_bootstrap_servers (str): The Kafka bootstrap servers address.
    - kafka_topic (str): The Kafka topic to subscribe to.

    Returns:
    - DataFrame: The streaming DataFrame.
    """
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .load()

    return df

# Parse the Kafka data
def parse_kafka_data(df, schema):
    """
    Parses the Kafka data into structured format based on the provided schema.

    Args:
    - df (DataFrame): The raw DataFrame from Kafka.
    - schema (str): The schema definition to parse the raw data.

    Returns:
    - DataFrame: The parsed DataFrame.
    """
    parsed_data = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
    return parsed_data

# Assemble features for anomaly detection
def assemble_features(df):
    """
    Assembles feature columns for anomaly detection.

    Args:
    - df (DataFrame): The parsed DataFrame containing sensor data.
    
    Returns:
    - DataFrame: The DataFrame with features assembled for anomaly detection.
    """
    assembler = VectorAssembler(inputCols=["temperature", "humidity", "pressure"], outputCol="features")
    transformed_data = assembler.transform(df)
    return transformed_data

# Predict anomalies using the trained Isolation Forest model
def predict_anomalies(batch_df, batch_id, trained_model):
    """
    Predicts anomalies in the incoming batch data.

    Args:
    - batch_df (DataFrame): The batch DataFrame to process and predict anomalies.
    - batch_id (str): A unique identifier for the batch.
    - trained_model (IsolationForest): The trained Isolation Forest model used for anomaly prediction.
    
    Saves anomalies to S3.
    """
    pandas_df = batch_df.select("temperature", "humidity", "pressure").toPandas()
    predictions = trained_model.predict(pandas_df)
    pandas_df["anomaly"] = predictions
    anomaly_df = spark.createDataFrame(pandas_df)
    
    # Save anomalies to S3
    anomaly_df.write.mode("append").parquet("s3://iot-sensor-anomaly-data/iot-anomalies/")
    anomaly_df.show()

# Main function to train the model and process streaming data
def main(kafka_bootstrap_servers, kafka_topic, historical_data):
    """
    Main function to train the model and process streaming data from Kafka.

    Args:
    - kafka_bootstrap_servers (str): The Kafka bootstrap servers address.
    - kafka_topic (str): The Kafka topic to subscribe to.
    - historical_data (pd.DataFrame): Historical IoT sensor data to train the model.

    Returns:
    - None
    """
    # Train Isolation Forest model
    trained_model = train_isolation_forest(historical_data)

    # Read and parse streaming data from Kafka
    df = read_kafka_stream(kafka_bootstrap_servers, kafka_topic)
    parsed_data = parse_kafka_data(df, schema)

    # Assemble features for anomaly detection
    transformed_data = assemble_features(parsed_data)

    # Process the streaming data and detect anomalies
    query = transformed_data.writeStream \
        .foreachBatch(lambda batch_df, batch_id: predict_anomalies(batch_df, batch_id, trained_model)) \
        .outputMode("append") \
        .start()

    query.awaitTermination()

# Sample historical data for training
historical_data = pd.DataFrame({
    "temperature": [22.5, 23.0, 21.8, 22.2, 23.1, 120.0],
    "humidity": [30, 32, 31, 33, 30, 10],
    "pressure": [1012, 1013, 1011, 1012, 1014, 950]
})

# Kafka connection details
kafka_bootstrap_servers = ""
kafka_topic = ""

# Run the anomaly detection pipeline
main(kafka_bootstrap_servers, kafka_topic, historical_data)
