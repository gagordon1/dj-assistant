from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

class MyLogger(object):
    def __init__(self, verbose = False):
        self.verbose = verbose
    def debug(self, msg):
        pass

    def warning(self, msg):
        if self.verbose:
            print(msg)

    def error(self, msg):
        print(msg)


"""
url : youtube link | soundcloud link
output_path : output path for the downloaded file

downloads a url and saves to a path
"""
def download(url, output_path, verbose = False):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '{}/%(title)s.%(ext)s'.format(output_path),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    'logger': MyLogger(verbose),
    }
    with YoutubeDL(ydl_opts) as ydl:
        if verbose:
            print("Downloading: {}".format(url))
        return ydl.download([url])

"""
Given a query, returns a list of video objects of the form :

{
    title : String,
    channelId : String
    id : String,
    thumbnail : String

  }
"""
def youtube_search(query):
    videos = VideosSearch(query, limit=5)
    return list(map(lambda x : {
        "title" : x["title"],
        "channelId" : x["channel"]["id"],
        "id" : x["id"],
        "thumbnail" : x["thumbnails"][0]["url"]
    },
    videos.result()["result"]))


if __name__ == '__main__':
    #download("https://www.youtube.com/watch?v=HYMDfMMD3fw", "ydl_test.mp3")
    # out = search("Everyday we lit")
    # print(out)
    pass
