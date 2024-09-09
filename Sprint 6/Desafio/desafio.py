import boto3 as b3
import datetime


# Constants of the project
BUCKET_NAME = "data-lake-do-gabriel-buron"
REGION_NAME = "us-east-2"

with open("credentials", "r") as f:
    PROFILE = f.readline()[1:][:-2]
date = datetime.datetime.now()

# Boto3 objects
session = b3.Session(profile_name=PROFILE)
print("Session Established")
s3 = session.resource("s3")
bucket = s3.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': REGION_NAME})
print("Bucket Created")

# Uploading files
bucket.upload_file("movies.csv",f"Raw/Local/CSV/Movies/{date.year}/{date.month}/{date.day}/movies.csv")
print("Movies Uploaded")
bucket.upload_file("series.csv",f"Raw/Local/CSV/Series/{date.year}/{date.month}/{date.day}/series.csv")
print("Series Uploaded")