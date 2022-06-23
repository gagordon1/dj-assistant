from flask import Flask, request
from operations import download_split_upload, download_upload, add_to_cache, get_from_cache, delete_file
from dotenv import load_dotenv
import uuid

load_dotenv()

app = Flask(__name__)
PORT=8000

@app.route('/')
def home():
    return 'Dj Assistant Backend Server :)'

"""
params :
    url : string youtube or soundcloud link

response :
    200 : {
        master : link to master mp3 file
        vocals : link to vocals mp3 file
        accompaniment : link to accompaniment mp3 file
    }
    400 : supplied link could not be split
"""
@app.route('/split/')
def split():
    try:
        url = request.args.get("url")
        links = get_from_cache(url, "all")
        if links:
            if links["vocals"] and links["accompaniment"]:
                return links
            else:
                #situation where we will overwrite the cached file
                delete_file(links["master"])
        pathname = str(uuid.uuid4())
        links = download_split_upload(url, pathname)
        if links:
            add_to_cache(url, links)
        return links

    except Exception as e:
        #delete created local files
        print(e)
        return "Supplied link could not be split", 400

"""
params :
    url : string youtube or soundcloud link

response :
    200 : {
        master : link to master mp3 file
    }
    400 : supplied link could not be returned
"""
@app.route('/download/')
def download():
    try:
        url = request.args.get("url")
        links = get_from_cache(url, "master")
        if links:
            return links

        pathname = str(uuid.uuid4())
        links = download_upload(url, pathname)
        if links:
            add_to_cache(url, links)
        return links

    except Exception as e:
        #delete created local files
        print(e)
        return "Supplied link could not be split", 400

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
