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

    processed_rows = []
    for row in rows:
        quantity_raw = row.get("quantity", "")
        price_raw = row.get("price", "")
        date_raw = row.get("order_date", "")

        quantity = int(quantity_raw) if quantity_raw else 0
        price = float(price_raw) if price_raw else 0.0
        try:
            order_date = datetime.strptime(date_raw, "%Y-%m-%d").date().isoformat() if date_raw else ""
        except ValueError:
            order_date = ""

        total_amount = quantity * price

        processed_row = {
            "order_id": row.get("order_id"),
            "order_date": order_date,
            "quantity": quantity,
            "price": price,
            "total_amount": total_amount
        }
        processed_rows.append(processed_row)

        output_lines = []
        fieldnames = processed_rows[0].keys()

        writer = csv.DictWriter(output_lines, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed_rows)

        output_csv = "\n".join(output_lines)
        output_key = key.replace("raw/", "processed/")

        s3.put_object(
            Bucket=bucket,
            Key=output_key,
            Body=output_csv.encode("utf-8")
        )

        print(f"Written cleaned file to s3://{bucket}/{output_key}")

