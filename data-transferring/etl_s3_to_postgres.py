import boto3
import pandas as pd
import psycopg2
from io import StringIO
import os
from dotenv import load_dotenv

#---- CONFIG ----
BUCKET = "bucket-rms-data"
REMOTE_KEY = "testing/test_sensor.csv"   # path inside S3 bucket

load_dotenv()
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "dbname": os.getenv("DB_NAME", "sensor_data"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "port": 5432
}

#---- EXTRACT ----
s3 = boto3.client("s3")
obj = s3.get_object(Bucket = BUCKET, Key=REMOTE_KEY)
df = pd.read_csv(
    obj["Body"],
    sep = ",",
    names=[
        "timestamp",
        "ina_current",
        "ina_voltage",
        "rpm",
        "lg_avg_speed",
        "wind_power"
    ],
    header=0
)

#---- TRANSFORM ----
df = df.replace({pd.NA: None})

#---- LOAD ----
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

for _, row in df.iterrows():
    cur.execute(
        """
        INSERT INTO sensor_readings
        (timestamp, ina_current, ina_voltage, rpm, lg_avg_speed, wind_power)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        tuple(row)
    )

conn.commit()
cur.close()
conn.close()

print("ETL completed successfully")