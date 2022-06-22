import boto3
import os
from dotenv import load_dotenv


load_dotenv()

ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ACCESS_ID = os.getenv("AWS_ACCESS_KEY_ID")
BUCKET = "dj-assistant-stems"

"""
file_path : input file path
bucket_file_path : desired filepath in the bucket

returns : True if successful upload, False otherwise
"""
def upload_to_amazon_bucket(file_path, bucket_file_path, verbose = False):
    try:
        if verbose:
            print("uploading to bucket...")
        s3 = boto3.resource('s3',
            aws_access_key_id=ACCESS_ID,
            aws_secret_access_key= ACCESS_KEY)
        s3.Bucket(BUCKET).upload_file(
            file_path,
            bucket_file_path,
            ExtraArgs = {
                "ContentType" : "audio/mp3"
                }
            )
        return True
    except Exception as e:
        print(e)
        return False
