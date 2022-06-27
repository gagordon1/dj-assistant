from flask import Flask, request
from operations import download_split_upload, download_upload, add_to_cache, get_from_cache, delete_file, delete_files_older_than
from dotenv import load_dotenv
import uuid
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS

SECONDS_IN_A_DAY = 86400
load_dotenv()

app = Flask(__name__)
PORT=8000

CORS(app)


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
    def garbage_collection():
        print("Starting Garbage Collection...")
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        #delete items that have been in the database for longer than x seconds
        delete_files_older_than(get_one_day_ago())



    def get_one_day_ago():
        return time.time() - SECONDS_IN_A_DAY

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=garbage_collection, trigger="interval", seconds=SECONDS_IN_A_DAY)
    scheduler.start()
    #
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    app.run(debug=False, port=PORT)
