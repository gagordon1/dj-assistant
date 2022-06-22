
from test_config import TEST_LINKS
from youtube import download
from splitter import split_file
import uuid
import os

if __name__ == '__main__':
    url = TEST_LINKS[0]
    ydl_path = "ydl/" + str(uuid.uuid4())
    #generate random folder to avoid collisions
    download(url, ydl_path)

    splits_path = "splits/" + str(uuid.uuid4())

    split_file(ydl_path + "/" + os.listdir(ydl_path)[0], splits_path)

    
