from yt_dlp import YoutubeDL

class MyLogger(object):
    def __init__(self, verbose = False):
        self.verbose = verbose
    def debug(self, msg):
        if self.verbose:
            print(msg)

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

if __name__ == '__main__':
    #download("https://www.youtube.com/watch?v=HYMDfMMD3fw", "ydl_test.mp3")
    pass
