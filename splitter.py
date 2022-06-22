from spleeter.separator import Separator
# can we get from youtube link to output?


def split_file(file, output_path):
    Separator('spleeter:2stems').separate_to_file(file, output_path)
