from flask import Flask, request
from youtube import download
from splitter import split_file
from aws_operations import upload_to_amazon_bucket
import uuid
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
PORT=8000
VERBOSE = True
AWS_BUCKET_ADDRESS = os.getenv("AWS_BUCKET_ADDRESS")
ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
ACCESS_ID = os.getenv("AWS_ACCESS_KEY_ID")
BUCKET = os.getenv("BUCKET_NAME")




@app.route('/')
def home():
    return 'Dj Assistant Backend Server :)'

"""
params :
    url : string youtube or soundcloud link

response :
    200 : link to directory on aws containing master.mp3, vocals.mp3 and accompaniment.mp3 files
    400 : supplied link could not be split
"""
@app.route('/split/')
def split():
    try:
        url = request.args.get("url")

        #generate random folder to avoid collisions
        pathname = str(uuid.uuid4())
        ydl_path = "ydl/" + pathname
        download(url, ydl_path, verbose = VERBOSE)

        stem_local_path = "stems/" + pathname
        bucket_file_path =  stem_local_path +".mp3"
        split_file(ydl_path + "/" + os.listdir(ydl_path)[0], stem_local_path, verbose = VERBOSE)

        #for vocals
        uploaded = upload_to_amazon_bucket(stem_local_path + "/vocals.mp3",
                bucket_file_path, ACCESS_KEY, ACCESS_ID, BUCKET, verbose = VERBOSE)

        #delete created local files
        shutil.rmtree(ydl_path)
        shutil.rmtree(stem_local_path)
        return AWS_BUCKET_ADDRESS + bucket_file_path
    except Exception as e:
        print(e)
        return "Supplied link could not be split", 400


    return bucket_file_path

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
