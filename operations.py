from resources.youtube import download
from resources.splitter import split_file
from resources.aws_operations import upload_to_amazon_bucket, upload_to_dynamo_cache, get_from_dynamo_cache, delete_amazon_bucket_file, get_killable_items, delete_dynamodb_item
import os
import shutil

VERBOSE = True
AWS_BUCKET_ADDRESS = os.getenv("AWS_BUCKET_ADDRESS")
ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ACCESS_ID = os.getenv("AWS_ACCESS_KEY_ID")
REGION = os.getenv("AWS_DEFAULT_REGION")
BUCKET = os.getenv("BUCKET_NAME")



"""
url : youtube or soundcloud link
pathname : unique identifier for intended bucket path of the file
returns {
    master : link to master mp3 file
    vocals : link to vocals mp3 file
    accompaniment : link to accompaniment mp3 file
}
"""
def download_split_upload(url, pathname):

    try:
        ydl_path = "ydl/" + pathname
        download(url, ydl_path, verbose = VERBOSE)

        stem_local_path = "stems/" + pathname

        download_name = os.listdir(ydl_path)[0]
        print(download_name)

        split_file(ydl_path + "/" + download_name, stem_local_path, verbose = VERBOSE)

        #for master track
        bucket_file_path_master =  stem_local_path +"/{}-master.mp3".format(download_name.strip(".mp3"))
        uploaded = upload_to_amazon_bucket(ydl_path + "/" + os.listdir(ydl_path)[0],
                bucket_file_path_master, ACCESS_KEY, ACCESS_ID, BUCKET, verbose = VERBOSE)

        #for vocals
        bucket_file_path_vocals =  stem_local_path +"/{}-vocals.mp3".format(download_name.strip(".mp3"))
        uploaded = upload_to_amazon_bucket(stem_local_path + "/vocals.mp3",
                bucket_file_path_vocals, ACCESS_KEY, ACCESS_ID, BUCKET, verbose = VERBOSE)

        #for accompaniment
        bucket_file_path_accompaniment =  stem_local_path +"/{}-accompaniment.mp3".format(download_name.strip(".mp3"))
        uploaded = upload_to_amazon_bucket(stem_local_path + "/accompaniment.mp3",
                bucket_file_path_accompaniment, ACCESS_KEY, ACCESS_ID, BUCKET, verbose = VERBOSE)

        #delete created local files
        shutil.rmtree(ydl_path)
        shutil.rmtree(stem_local_path)
        return {
                    "master" : AWS_BUCKET_ADDRESS + bucket_file_path_master,
                    "vocals" : AWS_BUCKET_ADDRESS + bucket_file_path_vocals,
                    "accompaniment" :  AWS_BUCKET_ADDRESS + bucket_file_path_accompaniment
                }
    except Exception as e:
        shutil.rmtree(ydl_path)
        shutil.rmtree(stem_local_path)
        print(e)
        raise e

"""
url : youtube or soundcloud link
pathname : unique identifier for intended bucket path of the file
returns {
    master : link to master mp3 file
}
"""
def download_upload(url, pathname):
    try:
        ydl_path = "ydl/" + pathname
        download(url, ydl_path, verbose = VERBOSE)
        download_name = os.listdir(ydl_path)[0]

        bucket_file_path_master =  "masters/" + pathname +"/{}-master.mp3".format(download_name)
        uploaded = upload_to_amazon_bucket(ydl_path + "/" + download_name,
                bucket_file_path_master, ACCESS_KEY, ACCESS_ID, BUCKET, verbose = VERBOSE)
        shutil.rmtree(ydl_path)
        return {"master" : AWS_BUCKET_ADDRESS + bucket_file_path_master}
    except Exception as e:
        print(e)
        shutil.rmtree(ydl_path)
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
return True if successful false otherwise
"""
def add_to_cache(url, links, region=REGION, verbose=VERBOSE):
    try:
        return upload_to_dynamo_cache(url, links, region, verbose)
    except Exception as e:
        print(e)
        return False

"""
Gets pointer to s3 database to avoid recomputing tracks

url : youtube or soundcloud link
type : String vocals | master | accompaniment | all
region : AWS region with dynamo db

return link or links if found, False otherwise
"""
def get_from_cache(url, type, region=REGION, verbose=VERBOSE):
    return get_from_dynamo_cache(url, type, region, verbose)

"""
Given an s3 link, remove it from our database

link : link to an s3 resource | False if file could not be deleted
"""
def delete_file(link, verbose=VERBOSE):
    try:
        if AWS_BUCKET_ADDRESS in link:
            key = "/".join(link.replace(AWS_BUCKET_ADDRESS, '').split("/")[:2])
            return delete_amazon_bucket_file(ACCESS_KEY, ACCESS_ID, BUCKET, key, verbose=VERBOSE)
        else:
            return False
    except Exception as e:
        print(e)
        return False

def delete_files_older_than(timestamp):
    killable = get_killable_items(timestamp)
    for item in killable:
        delete_file(item["master"]) #REMOVE S3 FILE
        delete_dynamodb_item(item["url"], REGION) #remove cache file




if __name__ == '__main__':

    # download_split_upload("https://www.youtube.com/watch?v=SKXDXMfcaP0", "test")
    pass
