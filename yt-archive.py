import csv 
import subprocess
import os 
import argparse

# parse out arguments
parser = argparse.ArgumentParser()
parser.add_argument("--channel-list", required=True, help="path to csv list of youtube channels")
parser.add_argument("--archive-location", default="archive.txt", help="location of yt-dlp archive file")
parser.add_argument("--save-location", default=".", help="folder to save your downloads")
args = vars(parser.parse_args())

channel_list_path = args["channel_list"]
archive_location = args["archive_location"]
folder_location = args["save_location"]



# read our channels.csv in to a list
with open(channel_list_path, "r") as f:
    reader = csv.reader(f)
    channel_list = list(reader)


# loop through each channel url
for channel in channel_list:
    url = channel[0]
    save_location = f"{folder_location}{channel[1].strip()}"
    
    # if directory doesn't exist, create it
    if not os.path.isdir(save_location):
        os.makedirs(save_location)
   # run yt_dlp 
    yt_dlp = subprocess.run(["yt-dlp", 
        "-P", f"{save_location}", 
        "--download-archive", f"{archive_location}", 
        f"{url}"])


# todo:build a new archive file from existing downloads
# todo:if no folder provided in csv, use channel name
# todo:generate log of activity/errors in a given run