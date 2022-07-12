from operations import delete_files_older_than
import time

SECONDS_IN_A_DAY = 86400

def get_one_day_ago():
    return time.time() - SECONDS_IN_A_DAY

def garbage_collection():
    print("Starting Garbage Collection...")
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    #delete items that have been in the database for longer than x seconds
    delete_files_older_than(get_one_day_ago())

if __name__ == '__main__':
    garbage_collection()
