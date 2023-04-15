import csv 
import subprocess
import os 
import argparse
from datetime import datetime
# parse out arguments
parser = argparse.ArgumentParser()
parser.add_argument("--channel-list", required=True, help="path to csv list of youtube channels")
parser.add_argument("--archive-location", default="archive.txt", help="location of yt-dlp archive file")
parser.add_argument("--save-location", default="", help="folder to save your downloads")
args = vars(parser.parse_args())

channel_list_path = args["channel_list"]
archive_location = args["archive_location"]
folder_location = args["save_location"]

file_name_format = "%(upload_date)s - %(title)s.%(ext)s"


# read our channels.csv in to a list
with open(channel_list_path, "r") as f:
    reader = csv.reader(f)
    channel_list = list(reader)


log_name = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".log"
log_path = folder_location + log_name
with open(log_path, "a") as f:
# loop through each channel url
    for channel in channel_list:
        
        url = channel[0]
        if folder_location == "":
            save_location = f"{channel[1].strip()}"
        else:
            # check for slash at the end of argument
            if folder_location[-1] != "/":
                folder_location = folder_location + "/"
            save_location = f"{folder_location}{channel[1].strip()}"
        
        # if directory doesn't exist, create it
        if not os.path.isdir(save_location):
            os.makedirs(save_location)
        
        # check for audio-only flag
        if channel[-1].strip() == "audio":
            file_name_format = "%(upload_date)s - %(title)s - audio.%(ext)s"
            # run yt_dlp 
            yt_dlp = subprocess.run(["yt-dlp", 
                "-P", f"{save_location}", 
                "--download-archive", f"{archive_location}",
                "-o", file_name_format,
                "-f", "ba", "--dateafter", "20230301",
                f"{url}"], stderr=f)
        else:
            file_name_format = "%(upload_date)s - %(title)s.%(ext)s"
            yt_dlp = subprocess.run(["yt-dlp", 
            "-P", f"{save_location}", 
            "--download-archive", f"{archive_location}",
            "-o", file_name_format, "--dateafter", "20230301",
            f"{url}"], stderr=f)
    
if os.path.getsize(log_path) == 0:
    os.remove(log_path)

# todo:build a new archive file from existing downloads
# todo:if no folder provided in csv, use channel name
# todo:generate log of activity/errors in a given run
# todo: add option to pass in additional yt-dlp params