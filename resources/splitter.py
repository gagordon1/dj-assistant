from spleeter.separator import Separator
import logging

# can we get from youtube link to output?
SAMPLE_RATE = 44100

"""
filename : input file as a string
destination_path : string
method : for now just ('spleeter:2stems')
type : "vocals" | "accompaniment"

Splits the file into vocals.mp3 and accompaniment.mp3 and saves
both into destination path
"""
def split_file(filename, destination_path, method="spleeter:2stems", verbose = False):
    if(verbose):
        print("splitting file {} to {}...".format(filename, destination_path))
    # Using embedded configuration.
    separator = Separator(method)
    print(separator)
    prediction = separator.separate_to_file(filename, destination_path,
        filename_format= "{instrument}.{codec}",  codec="mp3")
    print(prediction)

if __name__ == '__main__':
    # input_file = "ydl/3dedc6c2-d3bd-4451-9382-ea7462e5c7d6/Flo Rida - Right Round (feat. Ke$ha) [US Version] (Official Video).mp3"
    # dest_path = "./splits/MP3test"
    # split_file(input_file, dest_path)
    pass
