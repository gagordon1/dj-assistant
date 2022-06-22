
from test_config import TEST_LINKS
from youtube import download
from splitter import split_file
from aws_operations import upload_to_amazon_bucket
import uuid
import os


if __name__ == '__main__':
    url = TEST_LINKS[-2]
    verbose = True
    ydl_path = "ydl/" + str(uuid.uuid4())
    #generate random folder to avoid collisions
    download(url, ydl_path, verbose = verbose)

    filename = str(uuid.uuid4())
    local_path = "splits/" + filename
    bucket_file_path = "stems/" + filename +".mp3"

    split_file(ydl_path + "/" + os.listdir(ydl_path)[0], local_path, verbose = verbose)

    #for vocals
    uploaded = upload_to_amazon_bucket(local_path + "/vocals.mp3", bucket_file_path, verbose = verbose)

    # #for accompaniment
    # uploaded = upload_to_amazon_bucket(local_path + "/accompaniment.mp3", bucket_file_path, verbose = verbose)
