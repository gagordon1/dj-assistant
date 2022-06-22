
import youtube_dl
class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)



def download(url, output_path):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '{}/%(title)s.%(ext)s'.format(output_path),
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
        }],
    'logger': MyLogger(),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading: {}".format(url))
        return ydl.download([url])
