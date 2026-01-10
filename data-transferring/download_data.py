import boto3

BUCKET = "bucket-rms-data"
REMOTE_KEY = "raspi-data/sensor_data.csv"   # change later
LOCAL_FILE = "latest_data.csv"              # change later

def download():
    s3 = boto3.client("s3")
    s3.download_file(BUCKET, REMOTE_KEY, LOCAL_FILE)
    print("Downloaded latest sensor data.")

if __name__ == "__main__":
    download()
