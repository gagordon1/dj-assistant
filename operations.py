from resources.youtube import download
from resources.splitter import split_file
from resources.aws_operations import upload_to_amazon_bucket
import uuid
import os
import shutil

VERBOSE = True
AWS_BUCKET_ADDRESS = os.getenv("AWS_BUCKET_ADDRESS")
ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ACCESS_ID = os.getenv("AWS_ACCESS_KEY_ID")
BUCKET = os.getenv("BUCKET_NAME")


"""
url : youtube or soundcloud link
returns {
    master : link to master mp3 file
    vocals : link to vocals mp3 file
    accompaniment : link to accompaniment mp3 file
}
"""
def download_split_upload(url):

    try:
        #generate random folder to avoid collisions
        pathname = str(uuid.uuid4())
        ydl_path = "ydl/" + pathname
        download(url, ydl_path, verbose = VERBOSE)

        stem_local_path = "stems/" + pathname

        split_file(ydl_path + "/" + os.listdir(ydl_path)[0], stem_local_path, verbose = VERBOSE)

        #for master track
        bucket_file_path_master =  stem_local_path +"/master.mp3"
        uploaded = upload_to_amazon_bucket(ydl_path + "/" + os.listdir(ydl_path)[0],
                bucket_file_path_master, ACCESS_KEY, ACCESS_ID, BUCKET, verbose = VERBOSE)

        #for vocals
        bucket_file_path_vocals =  stem_local_path +"/vocals.mp3"
        uploaded = upload_to_amazon_bucket(stem_local_path + "/vocals.mp3",
                bucket_file_path_vocals, ACCESS_KEY, ACCESS_ID, BUCKET, verbose = VERBOSE)

        #for accompaniment
        bucket_file_path_accompaniment =  stem_local_path +"/accompaniment.mp3"
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
        raise e
