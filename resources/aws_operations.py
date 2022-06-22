import boto3

"""
Uploads an mp3 file to an aws bucket

file_path : input file path
bucket_file_path : desired filepath in the bucket
access_key : AWS access key
access_id : AWS access id
bucket : name of s3 bucket

returns : True if successful upload, False otherwise
"""
def upload_to_amazon_bucket(file_path, bucket_file_path, access_key, access_id, bucket, verbose = False):
    try:
        if verbose:
            print("uploading {} to bucket...".format(file_path))
        s3 = boto3.resource('s3',
            aws_access_key_id=access_id,
            aws_secret_access_key= access_key)
        s3.Bucket(bucket).upload_file(
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
