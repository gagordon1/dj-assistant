
from test_config import TEST_LINKS
from youtube import download
from splitter import split_file
from aws_operations import upload_to_amazon_bucket
import uuid
import os
import shutil


if __name__ == '__main__':
    url = TEST_LINKS[-2]
    verbose = True

    #generate random folder to avoid collisions
    pathname = str(uuid.uuid4())
    ydl_path = "ydl/" + pathname

    download(url, ydl_path, verbose = verbose)

    stem_local_path = "stems/" + pathname
    bucket_file_path =  stem_local_path +".mp3"

    split_file(ydl_path + "/" + os.listdir(ydl_path)[0], stem_local_path, verbose = verbose)

    #for vocals
    uploaded = upload_to_amazon_bucket(stem_local_path + "/vocals.mp3", bucket_file_path, verbose = verbose)

    #delete created local files
    shutil.rmtree(ydl_path)
    shutil.rmtree(stem_local_path)

    # #for accompaniment
    # uploaded = upload_to_amazon_bucket(local_path + "/accompaniment.mp3", bucket_file_path, verbose = verbose)
