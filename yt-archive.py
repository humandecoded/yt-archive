import csv 
import subprocess
import os 
import argparse
from datetime import datetime
# parse out arguments
parser = argparse.ArgumentParser()
parser.add_argument("--channel-list", required=True, help="path to csv list of youtube channels")
parser.add_argument("--archive-file", default="archive.txt", help="location of yt-dlp archive file")
parser.add_argument("--save-folder", default="", help="folder to save your downloads")
args = vars(parser.parse_args())

channel_list_path = args["channel_list"]
archive_file = args["archive_file"]
folder_location = args["save_folder"]

file_name_format = "%(upload_date)s - %(title)s.%(ext)s"


# read our channels.csv in to a list
with open(channel_list_path, "r") as f:
    reader = csv.reader(f)
    channel_list = list(reader)


log_name = datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + ".log"
log_path = folder_location + log_name
with open(log_path, "a") as f:
# loop through each channel url and its folder name
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
                "--download-archive", f"{archive_file}",
                "--match-filters", "availability=public",
                "-o", file_name_format,
                "-f", "ba", 
                f"{url}"], stderr=f, stdout=f)
        else:
            file_name_format = "%(upload_date)s - %(title)s.%(ext)s"
            yt_dlp = subprocess.run(["yt-dlp", 
            "-P", f"{save_location}", 
            "--download-archive", f"{archive_file}",
            "--match-filters", "availability=public",
            "-o", file_name_format,
            f"{url}"], stderr=f, stdout=f)

# parse out log to get errors we care about and downloads  
log_file_list = []
with open(log_path, "r") as f:
    for x in f.readlines():
        if "ERROR:" in x and "Private video" not in x and "Premier" not in x and "hidden" not in x:
            print("logging " + x)
            log_file_list.append(x.split(".")[0])
        elif "[download] Destination" in x:
            print("logging " + x)
            log_file_list.append(x.split(".")[0])

# get rid of duplicates
log_file_list = list(set(log_file_list))

# rewrite just the logs we parsed out above
with open(log_path, "w") as f:
    for line in log_file_list:
        f.write(f"{line}\n\n")
#delete file if no errors to report
if os.path.getsize(log_path) == 0:
    os.remove(log_path)

# todo:option to build out archive file without downwloading
# todo: add option to pass in additional yt-dlp params
# todo: explore importing yt-dlp as python library

