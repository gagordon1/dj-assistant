import boto3
import time
import os
from dotenv import load_dotenv
import json
load_dotenv()

def clean_url(url):
    if url[-1] == "/":
        url = url[:-1]
    return url

"""
Given an s3 key, remove it from our database

key : key to an s3 resource
"""
def delete_amazon_bucket_file(access_key, access_id, bucket, key, verbose=False):
    if verbose:
        print("Deleting {} from amazon s3 bucket...".format(key))
    s3 = boto3.resource('s3',
        aws_access_key_id=access_id,
        aws_secret_access_key= access_key)
    for file in ["/vocals.mp3", "/accompaniment.mp3", "/master.mp3"]:
        result = s3.Object(bucket, key + file).delete()
    if result:
        return True
    else:
        return False


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

"""
Uploads pointer to s3 database to avoid recomputing tracks

url : youtube or soundcloud link
links : associated s3 links of the form :
    {
        master : link to master mp3 file (required)
        vocals : link to vocals mp3 file (optional)
        accompaniment : link to accompaniment mp3 file (optional)
    }
region : AWS region with dynamo db

returns uploaded, throw exception otherwise
"""
def upload_to_dynamo_cache(url, links, region, verbose = False):
    if verbose:
        print("adding to dynamo cache")
    dynamodb = boto3.client("dynamodb", region_name=region)
    vocals = ""
    accompaniment = ""
    if "vocals" in links:
        vocals = links["vocals"]
    if "accompaniment" in links:
        accompaniment = links["accompaniment"]

    url = clean_url(url)

    dynamodb.put_item(TableName='dj-assistant-stem-cache',
         ReturnValues="ALL_OLD",
         Item={
            'url':{'S':url},
            'master':{'S':links["master"]},
            'vocals':{'S':vocals},
            'accompaniment':{'S':accompaniment},
            'timestamp_added':{'N' : str(time.time())}
        }
    )
    return True


"""
Gets pointer to s3 database to avoid recomputing tracks

url : youtube or soundcloud link
type : String vocals | master | accompaniment | all
region : AWS region with dynamo db

return link (or links if type is all) if found, False otherwise
"""
def get_from_dynamo_cache(url, type, region, verbose = False):
    if verbose:
        print("searching in dynamo cache")
    try:
        url = clean_url(url)
        dynamodb = boto3.client("dynamodb", region_name=region)
        result = dynamodb.get_item(TableName='dj-assistant-stem-cache',
            Key={
                "url" : {"S" : url}
            }
        )
        if "Item" in result:
            if type == "all":
                if verbose:
                    print("url was found in dynamo cache")
                return {
                    "vocals" : result["Item"]["vocals"]["S"],
                    "accompaniment" : result["Item"]["accompaniment"]["S"],
                    "master" : result["Item"]["master"]["S"]
                }
            else:
                if verbose:
                    print("url was found in dynamo cache")
                return {type : result["Item"][type]["S"]}
        else:
            if verbose:
                print("url was not found in dynamo cache")
            return False
    except Exception as e:
        if verbose:
            print("url was not found in dynamo cache")
        return False



if __name__ == '__main__':
    pass
