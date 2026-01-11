import csv
import boto3
from datetime import datetime

s3 = boto3.client("s3")


def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    print(f"Processing file: s3://{bucket}/{key}")
    response = s3.get_object(Bucket=bucket, Key=key)
    csv_bytes = response["Body"].read()
    csv_text = csv_bytes.decode("utf-8")

    reader = csv.DictReader(csv_text.splitlines())
    rows = list(reader)

    print(f"Rows read: {len(rows)}")
