from flask import Flask, request
from operations import download_split_upload
from dotenv import load_dotenv

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
        return download_split_upload(url)

    except Exception as e:
        #delete created local files
        print(e)
        return "Supplied link could not be split", 400

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
