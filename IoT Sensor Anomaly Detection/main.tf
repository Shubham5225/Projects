# Provider Configuration
provider "aws" {
  region = "us-east-1"
}

# Confluent Kafka Cluster (you need Confluent Cloud API keys and secrets)
resource "confluent_kafka_cluster" "iot_sensor_cluster" {
  display_name = "iot-sensor-cluster"
  availability = "STANDARD"
  cloud         = "AWS"
  region        = "us-east-1"
  version       = "latest"
}

resource "confluent_kafka_topic" "iot_sensor_topic" {
  display_name = "iot-sensor-stream"
  partition_count = 1
  replication_factor = 3
  kafka_cluster_id = confluent_kafka_cluster.iot_sensor_cluster.id
}

# S3 Bucket to store raw and anomaly data
resource "aws_s3_bucket" "iot_raw_data_bucket" {
  bucket = "iot-sensor-raw-data"
}

resource "aws_s3_bucket" "iot_anomaly_data_bucket" {
  bucket = "iot-sensor-anomaly-data"
}

# IAM Role for Glue to access S3 and Kafka
resource "aws_iam_role" "glue_role" {
  name               = "glue_streaming_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# Attach Policy to IAM Role to give it access to S3 and Kafka
resource "aws_iam_role_policy" "glue_role_policy" {
  name   = "glue-role-policy"
  role   = aws_iam_role.glue_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.iot_raw_data_bucket.arn}/*",
          "${aws_s3_bucket.iot_anomaly_data_bucket.arn}/*",
          "${aws_s3_bucket.iot_raw_data_bucket.arn}",
          "${aws_s3_bucket.iot_anomaly_data_bucket.arn}"
        ]
      },
      {
        Effect = "Allow"
        Action = "kafka:DescribeCluster"
        Resource = "*"
      }
    ]
  })
}

# Glue Job to process IoT Sensor Data and detect anomalies
resource "aws_glue_job" "iot_sensor_anomaly_job" {
  name     = "iot-sensor-anomaly-detection-job"
  role     = aws_iam_role.glue_role.arn
  command {
    name            = "glueetl"
    script_location = "scripts/iot_sensor_anomaly_detection.py"
  }
  max_capacity = 10
  glue_version = "2.0"
}

# Outputs
output "kafka_cluster_id" {
  value = confluent_kafka_cluster.iot_sensor_cluster.id
}

output "iot_raw_data_bucket" {
  value = aws_s3_bucket.iot_raw_data_bucket.bucket
}

output "iot_anomaly_data_bucket" {
  value = aws_s3_bucket.iot_anomaly_data_bucket.bucket
}

output "glue_job_name" {
  value = aws_glue_job.iot_sensor_anomaly_job.name
}
