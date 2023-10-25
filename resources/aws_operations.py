import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import os
from dotenv import load_dotenv
import json
from decimal import Decimal

CACHE_TABLE_NAME = 'dj-assistant-stem-cache'
load_dotenv()


def clean_url(url):
    if url[-1] == "/":
        url = url[:-1]
    return url

def delete_dynamodb_item(key, region):
    dynamodb = boto3.client("dynamodb", region_name=region)
    response = dynamodb.delete_item(TableName=CACHE_TABLE_NAME,
        Key={
            'url' : {'S' : key}
        }
    )


"""
Given an s3 key, remove each audio file along with their associated download file

key : key to an s3 resource
"""
def delete_amazon_bucket_file(access_key, access_id, bucket, key, verbose=False):
    if verbose:
        print("Deleting {} from amazon s3 bucket...".format(key))
    s3 = boto3.resource('s3',
        aws_access_key_id=access_id,
        aws_secret_access_key= access_key)
    result = s3.Object(bucket, key).delete()
    result = s3.Object(bucket, key + "/download.mp3").delete() #delete associated downloadable file

    if result:
        return True
    else:
        return False

"""
Uploads an mp3 file to an aws bucket
Also uploads a downloadable version with "/download.mp3" suffix

file_path : input file path
bucket_file_path : desired filepath in the bucket
access_key : AWS access key
access_id : AWS access id
bucket : name of s3 bucket

returns : True if successful upload, False otherwise
"""
def upload_to_amazon_bucket(file_path, bucket_file_path, access_key, access_id, bucket, region, verbose = False):
    try:
        if verbose:
            print("uploading {} to bucket...".format(file_path))
        name = bucket_file_path.split("/")[-1]
        print(name)
        disposition = 'attachment; filename=\"' + name
        s3 = boto3.resource('s3',
            aws_access_key_id=access_id,
            aws_secret_access_key= access_key,
            region_name=region
            )
        if verbose:
            print("connected to bucket",file_path, bucket_file_path, access_key, access_id, bucket, region)
            print("\n\n")

        s3.Bucket(bucket).upload_file(
            file_path,
            bucket_file_path,
            ExtraArgs = {
                "ContentType" : "audio/mp3"
                }
            )
        s3.Bucket(bucket).upload_file(
            file_path,
            bucket_file_path + "/download.mp3",
            ExtraArgs = {
                "ContentDisposition" : disposition
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
    print(region)
    vocals = ""
    accompaniment = ""
    if "vocals" in links:
        vocals = links["vocals"]
    if "accompaniment" in links:
        accompaniment = links["accompaniment"]

    url = clean_url(url)

    dynamodb.put_item(TableName=CACHE_TABLE_NAME,
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
        result = dynamodb.get_item(TableName=CACHE_TABLE_NAME,
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


"""
timestamp : time for which older items can be removed from the system
"""
def get_killable_items(timestamp):
    table = boto3.resource('dynamodb').Table(CACHE_TABLE_NAME)
    fe = Attr('timestamp_added').lt(Decimal(str(timestamp)))
    response = table.scan(
        FilterExpression=fe
    )
    return response['Items']

if __name__ == '__main__':
    # timestamp = get_one_day_ago()
    # killable = get_killable_items(timestamp)
    pass
