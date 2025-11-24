import boto3
from botocore.exceptions import ClientError

BUCKET = "bucket-rms-data"
LOCAL_FILE = "/home/pi/data/sensor_data.csv" # path inside the raspbery pi
REMOTE_KEY = "sensor-data/sensor.csv"   # path inside S3 bucket

def upload():
    s3 = boto3.client("s3")
    try:
        s3.upload_file(LOCAL_FILE, BUCKET, REMOTE_KEY)
        print("File uploaded successfully.")
    except ClientError as e:
        print("Upload failed:", e)

if __name__ == "__main__":
    upload()
